#include <err.h>
#include <float.h>
#include <stdio.h>
#include <stdlib.h>

#define PR_DO_MOVE 0.9
#define PR_STAY 0.1
#define PR_CORRECT_T 0.9
#define PR_INCORRECT_T 0.1
#define PR_OTHER 0.05

static unsigned int num_rows = 3;
static unsigned int num_cols = 3;
static unsigned int size = 9;

static struct node **__world;
static unsigned int num_unblocked;

enum terrain_type {
	N,
	H,
	T,
	B,
};

struct node {
	int x;
	int y;
	enum terrain_type type;
};

struct world_file_results {
	struct node **nodes;
	int num_unblocked;
};

static enum terrain_type char_to_type(char c)
{
	if (c == 'N')
		return N;
	if (c == 'H')
		return H;
	if (c == 'T')
		return T;
	if (c == 'B')
		return B;
}

static inline int type_delta_x(char a)
{
	if (a == 'U')
		return -1;
	if (a == 'D')
		return 1;
	return 0;
}

static inline int type_delta_y(char a)
{
	if (a == 'L')
		return -1;
	if (a == 'R')
		return 1;
	return 0;
}

static void point_mult(double *v1, double *v2, int v1_len, int v2_len)
{
	int i;

	if (v1_len == v2_len) {
		for (i = 0; i < v1_len; i++)
			v1[i] *= v2[i];
	} else if (v1_len == 1) {
		for (i = 0; i < v2_len; i++)
			v1[0] *= v2[i];
	} else if (v2_len == 1) {
		double *v1p = v1;
		double v2_val = *v2;
		for (i = 0; i < v1_len; i++)
			*v1++ *= v2_val;
	} else {
		errx(1, "Gave bad input to point mult"
			" params (v1_len, v2_len) = (%d, %d)",
			v1_len, v2_len);
	}
}

static struct world_file_results parse_world_file(const char *file)
{
	struct world_file_results ret = {0};
	struct node **world, *row;
	FILE *fp;
	char buf[4096];
	char *start, *end;
	int i = 0, so_far = 0;

	fp = fopen(file, "r");
	if (!fp)
		err(1, "C Error opening %s", file);

	fgets(buf, 4096, fp);
	start = buf;
	num_rows = strtol(start, &end, 10);
	start = end;
	num_cols = strtol(start, &end, 10);
	size = num_rows * num_cols;

	world = malloc(sizeof(*world) * num_rows);
	ret.nodes = world;
	row = malloc(sizeof(*row) * num_cols);
	while (fgets(buf, 4096, fp)) {
		struct node *n;
		int row_num, col_num;
		char type;
		start = buf;
		row_num = strtol(start, &end, 10);
		start = end;
		col_num = strtol(start, &end, 10);
		type = *++end;


		row[i].x = row_num;
		row[i].y = col_num;
		row[i].type = char_to_type(type);
		if (row[i].type != B)
			ret.num_unblocked++;
		i++;
		if (++so_far == num_cols) {
			*world++ = row;
			row = malloc(sizeof(*row) * num_cols);
			i = 0;
			so_far = 0;
		}
	}

	world = ret.nodes;
	fclose(fp);
	return ret;
}

static double *init_distr(int num_unblocked)
{
	double *distr, val;
	int i;

	distr = malloc(sizeof(*distr) * size);
	val = 1.0 / num_unblocked;
	for (i = 0; i < size; i++)
		distr[i] = val;
	return distr;
}

static inline int in_bounds(int row, int col)
{
	return row >= 0 && row < num_rows && col >= 0 && col < num_cols;
}

struct trans_result {
	double res1;
	double res2;
	int pos1;
	int pos2;
};

static struct trans_result transition(double *t, struct node **world,
		struct node *c, char action)
{
	static int counter;
	struct trans_result trans_result;
	int destx, desty;

	destx = c->x + type_delta_x(action);
	desty = c->y + type_delta_y(action);

	if (!in_bounds(destx - 1, desty - 1) || world[destx - 1][desty - 1].type == B) {
		//t[(num_cols * (c->x - 1)) + (c->y - 1)] = 1.0;
		trans_result.res1 = 1.0;
		trans_result.pos1 = (num_cols * (c->x - 1)) + (c->y - 1);
		trans_result.res2 = 0.0;
		trans_result.pos2 = 0;
		//printf("so far: %d\n", ++counter);
	} else {
		//t[(num_cols * (c->x - 1)) + (c->y - 1)] = PR_STAY;
		//t[(num_cols * (destx - 1)) + (desty - 1)] = PR_DO_MOVE;
		trans_result.res1 = PR_STAY;
		trans_result.pos1 = (num_cols * (c->x - 1)) + (c->y - 1);
		trans_result.res2 = PR_DO_MOVE;
		trans_result.pos2 = (num_cols * (destx - 1)) + (desty - 1);
	}
	return trans_result;
}

static void scalar_mult(struct trans_result *tr, double t)
{
	tr->res1 *= t;
	tr->res2 *= t;
}

static void add_scaled_trans(struct trans_result *tr, double *sum)
{
	sum[tr->pos1] += tr->res1;
	sum[tr->pos2] += tr->res2;
}

static void observation(struct node **world, double *obs, enum terrain_type sensed)
{
	int i;
	for (i = 0; i < size; i++) {
		struct node *n = &world[i / num_cols][i % num_cols];
		if (n->type == B)
			obs[i] = 0.0;
		else if (n->type == sensed)
			obs[i] = PR_CORRECT_T;
		else
			obs[i] = PR_OTHER;
	}
}

static void print_vector(double *p, unsigned long size)
{
	unsigned long i;

	printf("[ ");
	for (i = 0; i < size; i++)
		printf("%g, ", p[i]);
	printf(" ]\n");
}

static double *do_filter(struct node **world, const char state,
		const char action, double *prev)
{
	double *summation, *trans_model, *obs, *normalized_factor;
	double summ_res;
	int i, j, idx;

	if (!state || !action)
		return NULL;

	trans_model = calloc(size, sizeof(double));
	obs = calloc(size, sizeof(double));
	summation = calloc(size, sizeof(double));
	normalized_factor = calloc(size, sizeof(double));
	for (j = 0, idx = 0; j < size; j++, idx++) {
		struct node *curr = &world[j / num_cols][j % num_cols];
		struct trans_result tr = {0};

		if (curr->type == B)
			continue;
		tr = transition(trans_model, world, curr, action);
		scalar_mult(&tr, prev[idx]);
		add_scaled_trans(&tr, summation);
	}
	observation(world, obs, char_to_type(state));
	point_mult(summation, obs, size, size);
	for (summ_res = 0, i = 0; i < size; i++)
		summ_res += summation[i];
	for (i = 0; i < size; i++)
		normalized_factor[i] = 1.0 / summ_res;
	point_mult(summation, normalized_factor, size, size);
	free(obs);
	free(trans_model);
	free(normalized_factor);
	return summation;
}

unsigned int load_world(const char *world_file)
{
	struct world_file_results ret;

	ret = parse_world_file(world_file);
	__world = ret.nodes;
	num_unblocked = ret.num_unblocked;
	return size;
}

double *filter_step(char sensor_data, char action, double *prev)
{
	if (!prev)
		prev = init_distr(num_unblocked);
	return do_filter(__world, sensor_data, action, prev);
}
