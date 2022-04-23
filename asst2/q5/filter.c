#include <err.h>
#include <float.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define bad_malloc(size)						\
	err(1, "%s [Line: %d] - malloc error() allocating %zu bytes",	\
			__func__, __LINE__, size)

/* Probability that we execute a move */
#define PR_DO_MOVE 0.9

/* Probability that we stay at our current position */
#define PR_STAY 0.1

/* Probability that we correctly sense the terrain */
#define PR_CORRECT_T 0.9

/*
 * Probability that we sensed an incorrect reading, but we are on the
 * correct cell. Example: P(Not sensing N | Cell is N) = 0.1
 */
#define PR_INCORRECT_T 0.1

/*
 * Probability that we sense an incorrect reading, but we are on a non
 * matching cell. Example: P(Sensing N | Cell is not N) = 0.05
 */
#define PR_OTHER 0.05

static unsigned int num_rows = 3;
static unsigned int num_cols = 3;

/*
 * Size of the graph (number of nodes)
 * num_rows * num_cols
 */
static unsigned int size = 9;

/* The "world" denoted by a 2d array of cells */
static struct node **__world;

/* Number of unblocked cells in the world */
static unsigned int num_unblocked;

/* Type of the terrain */
enum terrain_type {
	N, /* Normal */
	H, /* Highway */
	T, /* Tought to Traverse */
	B, /* Blocked */
};

/*
 * Node on the grid
 *
 * IMPORTANT NOTE: These x,y coordinates start at 1,1. This detail is why
 * some coordinate code has '-1' attached to it.
 */
struct node {
	int x;
	int y;
	enum terrain_type type;
};

/* Results from parsing a world file */
struct world_file_results {
	struct node **nodes;
	int num_unblocked;
};

/* Convert character to respective type */
static enum terrain_type char_to_type(char c)
{
	switch (c) {
	case 'N':
		return N;
	case 'H':
		return H;
	case 'T':
		return T;
	case 'B':
		return B;
	default:
		errx(-1, "Passed in bad value (%d) to %s\n", c, __func__);
	}
}

static inline int is_valid_terrain_type(char c)
{
	return c == 'N' || c == 'H' || c == 'T' || c == 'B';
}

static inline int is_valid_action(char c)
{
	return c == 'U' || c == 'D' || c == 'L' || c == 'R';
}

/* The change of x coordinate given an action */
static inline int type_delta_x(char a)
{
	switch (a) {
	case 'U':
		return -1;
	case 'D':
		return 1;
	default:
		return 0;
	}
}

/* The change of y coordinate given an action */
static inline int type_delta_y(char a)
{
	switch (a) {
	case 'L':
		return -1;
	case 'R':
		return 1;
	default:
		return 0;
	}
}

/*
 * Point multiplcation
 *
 * NOTE: The result of this multiplcation is stored within v1
 */
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
		double v2_val = *v2;
		for (i = 0; i < v1_len; i++)
			*v1++ *= v2_val;
	} else {
		errx(1, "Gave bad input to point mult"
			" params (v1_len, v2_len) = (%d, %d)",
			v1_len, v2_len);
	}
}


/*
 * Parse the world file
 */
static struct world_file_results parse_world_file(const char *file)
{
	struct world_file_results ret = {0};
	struct node **world, *row;
	FILE *fp;
	char buf[4096];
	char *start, *end;
	unsigned int nodes_read = 0;
	int i = 0, so_far = 0;

	fp = fopen(file, "r");
	if (!fp)
		err(1, "Error opening %s", file);

	/*
	 * Read in the first line which has our measurements of the world.
	 * The first line should be like: "NUM_ROWS NUM_COLS" where they are
	 * numbers.
	 */
	if (!fgets(buf, sizeof(buf), fp))
		err(1, "Failed to read first line of file for size. "
			"Ensure file is correctly formatted.");
	start = buf;
	num_rows = strtol(start, &end, 10);
	if (num_rows == LONG_MIN || num_rows == LONG_MAX || start == end)
		err(1, "Failed to read in number of rows from file. "
			"Contents of line:\n\t%s", buf);
	start = end;
	num_cols = strtol(start, &end, 10);
	if (num_cols == LONG_MIN || num_cols == LONG_MAX || start == end)
		err(1, "Failed to read in number of columns from file. "
			"Contents of line:\n\t%s", buf);

	size = num_rows * num_cols;
	world = malloc(sizeof(*world) * num_rows);
	if (!world)
		bad_malloc(sizeof(*world) * num_rows);
	ret.nodes = world;
	row = malloc(sizeof(*row) * num_cols);
	if (!row)
		bad_malloc(sizeof(*row) * num_cols);

	/*
	 * The rest of the file is simply in the form: X Y T
	 * where X is the x coordinate, Y is the y coordinate, and T
	 * is the type of terrain at those coordinates.
	 */
	while (fgets(buf, sizeof(buf), fp)) {
		struct node *n = &row[i];
		int row_num, col_num;
		char type;
		start = buf;
		row_num = strtol(start, &end, 10);
		if (row_num == LONG_MIN || row_num == LONG_MAX || start == end)
			err(1, "Failed to read in x coordinate of node. "
				"Contents of line:\n\t%s", buf);
		start = end;
		col_num = strtol(start, &end, 10);
		if (col_num == LONG_MIN || col_num == LONG_MAX || start == end)
			err(1, "Failed to read in y coordinate of node. "
				"Contents of line:\n\t%s", buf);

		type = *++end;
		if (!is_valid_terrain_type(type))
			errx(1, "Failed to retrieve valid terrain type from line. "
				"Got %c (val: %d) from line:\n\t%s",
				type, type, buf);

		n->x = row_num;
		n->y = col_num;
		n->type = char_to_type(type);
		if (n->type != B)
			ret.num_unblocked++;
		i++;
		nodes_read++;

		/*
		 * If the number of lines so far is equal to the number of
		 * columns, we are finished with that row.
		 */
		if (++so_far == num_cols) {
			*world++ = row;
			row = malloc(sizeof(*row) * num_cols);
			if (!row)
				bad_malloc(sizeof(*row) * num_cols);
			i = 0;
			so_far = 0;
		}
	}
	if (nodes_read != size)
		errx(1, "Read only %u nodes, when file said to expect %d cells.",
				nodes_read, size);
	world = ret.nodes;
	fclose(fp);
	return ret;
}

/*
 * Calculate the initial distribution of the world
 */
static double *init_distr(int num_unblocked)
{
	double *distr, val;
	int i;

	distr = malloc(sizeof(*distr) * size);
	if (!distr)
		bad_malloc(sizeof(*distr) * size);
	val = 1.0 / num_unblocked;
	for (i = 0; i < size; i++)
		distr[i] = val;
	return distr;
}

/*
 * Check if the requested row and column is in bounds
 */
static inline int in_bounds(int row, int col)
{
	return row >= 0 && row < num_rows && col >= 0 && col < num_cols;
}

/*
 * The result of the transition.
 * Stores two results.
 */
struct trans_result {
	double res1;
	double res2;
	int pos1;
	int pos2;
};

/*
 * Calcualte the transition matrix. In the filter equation: P(X_t | X_t-1)
 *
 * NOTE: This is optimized. The actual transition matrix should be a matrix of
 * [num_rows x num_cols]. However, this matrix will only EVER hold 2 values.
 * Therefore, it is full of zeros besides 2 spots. Therefore, we only pass back
 * the two indicies and their relevant values instead of filling in an array with
 * all zeros but two spots.
 */
static void transition(struct trans_result *tr, struct node **world,
			struct node *c, char action)
{
	int destx, desty;

	destx = c->x + type_delta_x(action);
	desty = c->y + type_delta_y(action);

	if (!in_bounds(destx - 1, desty - 1) || world[destx - 1][desty - 1].type == B) {
		tr->res1 = 1.0;
		tr->pos1 = (num_cols * (c->x - 1)) + (c->y - 1);
		tr->res2 = 0.0;
		tr->pos2 = 0;
	} else {
		tr->res1 = PR_STAY;
		tr->pos1 = (num_cols * (c->x - 1)) + (c->y - 1);
		tr->res2 = PR_DO_MOVE;
		tr->pos2 = (num_cols * (destx - 1)) + (desty - 1);
	}
}

/*
 * Scalar multiplication for the results from the transition matrix.
 */
static void scalar_mult(struct trans_result *tr, double t)
{
	tr->res1 *= t;
	tr->res2 *= t;
}

/*
 * Add the scaled transition values to the summation array.
 */
static void add_scaled_trans(struct trans_result *tr, double *sum)
{
	sum[tr->pos1] += tr->res1;
	sum[tr->pos2] += tr->res2;
}

/*
 * Fill in the observation matrix with the relevant probabilities of reading
 * correctly.
 */
static void observation(struct node **world, double *obs, enum terrain_type sensed)
{
	int i;
	for (i = 0; i < size; i++) {
		struct node *n = &world[i / num_cols][i % num_cols];
		/* Blocked cells cant be observed */
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

/*
 * do_filter - Compute a single iteration of the Bayesian Network Filter
 *
 * Note: Returns a malloc'd array holding our result.
 *
 * Filter Equation:
 * P(X_t | E_1:t) = @ P(E_t | X_t) Σ_{X_t-1} P(X_t | X_t-1) * P(X_t-1 | E_1:t-1)
 *
 * Symbols:
 * 	@ - Alpha (Normalizing factor)
 *
 * 	P(E_t | X_t) - Observation model (Matrix of probability we sensed right)
 *
 * 	P(X_t | X_t-1) - Transition model (Matrix of probability we get to X_t
 * 		from X_t-1)
 *
 * 	P(X_t-1 | E_1:t-1) - Previous model (Matrix of the probability
 * 		distribution from the previous iteration)
 */
static double *do_filter(struct node **world, const char sensor,
		const char action, double *prev)
{
	double *summation, *trans_model, *obs;
	double alpha;
	int i;

	/* Might want to actually throw some type of error for this if... */
	if (!world || !prev || !is_valid_terrain_type(sensor) || !is_valid_action(action))
		return NULL;

	/* Transition matrix */
	trans_model = calloc(size, sizeof(double));
	if (!trans_model)
		bad_malloc(size * sizeof(double));

	/* Observation matrix */
	obs = calloc(size, sizeof(double));
	if (!obs)
		bad_malloc(size * sizeof(double));

	/* Summation result */
	summation = calloc(size, sizeof(double));
	if (!summation)
		bad_malloc(size * sizeof(double));

	/* This for loop calculates the summation part of the equation */
	for (i = 0; i < size; i++) {
		struct node *curr = &world[i / num_cols][i % num_cols];
		struct trans_result tr;

		/* Disregard blocked cells */
		if (curr->type == B)
			continue;
		memset(&tr, 0, sizeof(tr));

		/* P(X_t | X_t-1) */
		transition(&tr, world, curr, action);
		/* P(E_t | X_t) * P(X_t-1 | E_1:t-1) */
		scalar_mult(&tr, prev[i]);
		/* Summate to running total matrix */
		add_scaled_trans(&tr, summation);
	}
	/* P(E_t | X_t) */
	observation(world, obs, char_to_type(sensor));
	/* P(E_t | X_t) * Summation result */
	point_mult(summation, obs, size, size);

	/* Calculate normalization */
	alpha = 0;
	for (i = 0; i < size; i++)
		alpha += summation[i];
	alpha = 1.0 / alpha;

	/* Normalize the result */
	for (i = 0; i < size; i++)
		summation[i] *= alpha;

	free(obs);
	free(trans_model);
	return summation;
}

/*
 * Call point for python to load the world file.
 *
 * Returns the size of the world (num_rows * num_cols)
 */
unsigned int load_world(const char *world_file)
{
	struct world_file_results ret;

	ret = parse_world_file(world_file);
	__world = ret.nodes;
	num_unblocked = ret.num_unblocked;
	return size;
}

/*
 * Call point for python to do a single step of filtering.
 *
 * @prev being NULL denotes that we should use the inital distribution
 */
double *filter_step(char sensor_data, char action, double *prev)
{
	if (!__world)
		errx(1, "Call load_world() before trying to do filter_step!");
	if (!prev)
		prev = init_distr(num_unblocked);
	return do_filter(__world, sensor_data, action, prev);
}
