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
    if random.random() > val:
        return "~" + idx_to_node(idx)
    return idx_to_node(idx)

def get_nested_value(idx, evidence):
    val = arr[idx][evidence]
    if random.random() > val:
        return "~" + idx_to_node(idx)
    return idx_to_node(idx)

def do_rejection(want, evidence):
    good_samples = 0
    success = 0
    fails = 0

    f = open("rejection_sample.txt", "w")
    f.write("Sample_Number, Probability\n")
    for i in range(NUM_SAMPLES):
        a_res = get_parent_value(0)
        b_res = get_parent_value(1)
        c_res = get_nested_value(2, a_res + b_res)
        d_res = get_nested_value(3, b_res + c_res)
        complete = a_res + b_res + c_res + d_res
        if evidence in complete and ("~" + evidence) not in complete: # Rejection
            good_samples += 1
            want_res = ""

            if want in a_res:
                want_res = a_res
            elif want in b_res:
                want_res = b_res
            elif want in c_res:
                want_res = c_res
            elif want in d_res:
                want_res = d_res

            if "~" not in want_res:
                success += 1
            else:
                fails += 1
        f.write(str(i) + "," + (str(success / good_samples) if good_samples != 0 else "0") + "\n")
    f.close()
    print("Rejection samples <succ, fails> : <" +
            str(success / good_samples) + ", " +
            str(fails / good_samples) + ">")

def main():
    do_rejection("d", "~ab~c")

if __name__ == "__main__":
    main()
