import random
NUM_SAMPLES = 1000
arr = [dict() for x in range(4)]

arr[0] = {"a": 0.00}
arr[1] = {"b": 0.90}
arr[2] = {"ab": 0.20, "a~b": 0.60, "~ab": 0.50, "~a~b": 0.00}
arr[3] = {"bc": 0.75, "b~c": 0.10, "~bc": 0.50, "~b~c": 0.20}

def idx_to_node(idx) -> str:
    if idx == 0:
        return "a"
    elif idx == 1:
        return "b"
    elif idx == 2:
        return "c"
    elif idx == 3:
        return "d"

def get_parent_value(idx):
    val = arr[idx][idx_to_node(idx)]
    notation = idx_to_node(idx)
    if random.random() > val:
        notation = "~" + idx_to_node(idx)
        val = 1 - val
    return (notation, val)

def get_nested_value(idx, evidence):
    val = arr[idx][evidence]
    notation = idx_to_node(idx)
    if random.random() > val:
        notation = "~" + idx_to_node(idx)
        val = 1 - val
    return (notation, val)

# If evidence variable
#   w *= P(var)
#       --> NOTICE: var would be whatever it is set to in evidence
# If not evidence
#   Simply do the get_parent/nested_value
#
# THEN: add our result weight to a True/False counter vector
def do_weighted(want, evidence):
    vec = [0.0, 0.0]

    f = open("weighted_sample.txt", "w")
    f.write("Sample_Number, Probability\n")
    for i in range(NUM_SAMPLES):
        weight = 1
        if "a" not in evidence:
            a_res = get_parent_value(0)
        else:
            if "~a" in evidence:
                a_res = ("~a", 1 - arr[0]["a"])
            else:
                a_res = ("a", arr[0]["a"])
            weight *= a_res[1]

        if "b" not in evidence:
            b_res = get_parent_value(1)
        else:
            if "~b" in evidence:
                b_res = ("~b", 1 - arr[1]["b"])
            else:
                b_res = ("b", arr[1]["b"])
            weight *= b_res[1]

        if "c" not in evidence:
            c_res = get_nested_value(2, a_res[0] + b_res[0])
        else:
            if "~c" in evidence:
                c_res = ("~c", 1 - arr[2][a_res[0] + b_res[0]])
            else:
                c_res = ("c", arr[2][a_res[0] + b_res[0]])
            weight *= c_res[1]

        if "d" not in evidence:
            d_res = get_nested_value(3, b_res[0] + c_res[0])
        else:
            if "~d" in evidence:
                d_res = ("~d", 1 - arr[3][b_res[0] + c_res[0]])
            else:
                d_res = ("d", arr[3][b_res[0] + c_res[0]])
            weight *= d_res[1]

        vec_index = 0
        if "a" in want:
            if "a" != a_res[0]:
                vec_index = 1
        elif "b" in want:
            if "b" != b_res[0]:
                vec_index = 1
        elif "c" in want:
            if "c" != c_res[0]:
                vec_index = 1
        elif "d" in want:
            if "d" != d_res[0]:
                vec_index = 1

        vec[vec_index] += weight
        f.write(str(i) + "," + str(vec[0] / (vec[0] + vec[1])) + "\n")
    f.close()
    print("Weighting: < " + str(vec[0] / (vec[0] + vec[1])) +
            ", " + str(vec[1] / (vec[0] + vec[1])))


def main():
    do_weighted("d", "~ab~c")

if __name__ == "__main__":
    main()
