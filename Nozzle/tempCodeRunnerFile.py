def k_factor(k, tdl_orifice_num, x, y, z):

    for n in tdl_orifice_num:
        if n == k:
            return x * n ** 2 - y * n + z