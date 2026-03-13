# =========================
# SIZE SPLIT
# =========================

def size_split(colors, pieces, sizes, ratios):

    total_ratio = sum(ratios)

    split_result = {}

    for color, pcs in zip(colors, pieces):

        split_result[color] = {}

        for size, ratio in zip(sizes, ratios):

            split_value = int(pcs * ratio / total_ratio)

            split_result[color][size] = split_value

    return split_result


# =========================
# PACKING ENGINE
# =========================

def packing_engine(size_split_data):

    sizes = list(next(iter(size_split_data.values())).keys())
    colors = list(size_split_data.keys())

    results = []

    for size in sizes:

        remaining = []

        for color in colors:
            remaining.append(size_split_data[color][size])

        color_count = len(colors)

        # TRUE COMBO
        true_boxes = min(remaining)

        structure = " + ".join([f"1 {c}" for c in colors])

        size_result = {
            "size": size,
            "true_boxes": true_boxes,
            "true_structure": structure,
            "secondary": [],
            "remaining": {}
        }

        for i in range(color_count):
            remaining[i] -= true_boxes

        # =========================
        # SECONDARY COMBO
        # =========================

        active_colors = 0
        least_remain = 999999

        for r in remaining:

            if r > 0:

                active_colors += 1

                if r < least_remain:
                    least_remain = r

        box_size = color_count

        if active_colors >= box_size - 1:

            sec_boxes = least_remain

            while True:

                extras_needed = sec_boxes
                extras_available = 0

                for r in remaining:

                    if r > sec_boxes:
                        extras_available += (r - sec_boxes)

                if extras_available >= extras_needed:
                    break

                sec_boxes -= 1

                if sec_boxes == 0:
                    break

            if sec_boxes > 0:

                extra_pattern = [0] * color_count
                extras_left = sec_boxes

                for i in range(color_count):

                    if remaining[i] > sec_boxes:

                        possible = remaining[i] - sec_boxes
                        used = min(possible, extras_left)

                        extra_pattern[i] = used
                        extras_left -= used

                        if extras_left == 0:
                            break

                for i in range(color_count):

                    if extra_pattern[i] > 0:

                        structure = ""

                        for k in range(color_count):

                            if remaining[k] > 0:

                                if k == i:
                                    structure += f"2 {colors[k]} + "
                                else:
                                    structure += f"1 {colors[k]} + "

                        structure = structure[:-3]

                        size_result["secondary"].append({
                            "boxes": extra_pattern[i],
                            "structure": structure
                        })

                for i in range(color_count):

                    if remaining[i] > 0:
                        remaining[i] -= sec_boxes

                    remaining[i] -= extra_pattern[i]

        # =========================
        # FINAL REMAINING
        # =========================

        for c, r in zip(colors, remaining):
            size_result["remaining"][c] = r

        results.append(size_result)

    return results


# =========================
# TEST RUN
# =========================

if __name__ == "__main__":

    colors = ["Red", "Blue", "Black"]
    pieces = [100, 120, 110]

    sizes = ["S", "M", "L"]
    ratios = [1, 2, 1]

    split_data = size_split(colors, pieces, sizes, ratios)

    # =========================
    # PRINT SIZE SPLIT
    # =========================

    print("\n==============================")
    print("SIZE SPLIT")
    print("==============================")

    header = "Color".ljust(10)

    for s in sizes:
        header += s.rjust(8)

    print(header)
    print("-" * len(header))

    for color in colors:

        row = color.ljust(10)

        for size in sizes:
            row += str(split_data[color][size]).rjust(8)

        print(row)

    # =========================
    # RUN PACKING
    # =========================

    results = packing_engine(split_data)

    for r in results:

        print("\n==============================")
        print("SIZE", r["size"])
        print("==============================")

        print("\nTRUE COMBO")
        print("Boxes:", r["true_boxes"])
        print("Structure:", r["true_structure"])

        if r["secondary"]:

            print("\nSECONDARY COMBO")

            for s in r["secondary"]:

                print("Boxes:", s["boxes"])
                print("Structure:", s["structure"])

        print("\nREMAINING AFTER PACKING")

        for c, v in r["remaining"].items():
            print(c, ":", v)