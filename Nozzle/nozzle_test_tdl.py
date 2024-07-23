from tabulate import tabulate

tdl_num_nozzles = int(input("Number of Nozzles: "))
swirl_input = input("Enter swirl number (e.g., SWL1, SWL2, etc.): ")
k = float(input("Orifice Number: "))

tdl_orifice_num = [18, 20, 22, 24, 27, 30, 33, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58]

tdl_operating_pressure = float(input("Operating Pressure: "))
tdl_lsg = float(input("Liquid Specific Gravity: "))
tdl_spa = input("Spray Angle: ")
tdl_lpcs = float(input("Liquid Per Cent Solids: "))
tdl_ppcm = float(input("Powder Per Cent Moisture: "))


def k_factor(k, tdl_orifice_num, x, y, z):

    for n in tdl_orifice_num:
        if n == k:
            return x * n ** 2 - y * n + z

def k_factor(k, orifice_num, x, y, z):
    for n in orifice_num:
        if n == k:
            return x * n ** 2 + y * n - z
    return None


k1 = k_factor(k, tdl_orifice_num, -0.00312, -0.4741, -3.90283)
k2 = k_factor(k, tdl_orifice_num, 0.00166, -0.24556, 0.36082)
k3 = k_factor(k, tdl_orifice_num, -0.0214, -2.9143, -71.774)
k4 = k_factor(k, tdl_orifice_num, 0.00938, 0.23464, 4.07737)

# print(k4, k1, k2, k3)

sfor4 = None
sfor1 = None
sfor2 = None
sfor3 = None

def screen_for_orifice_range(k, tdl_orifice_num):
    global sfor4, sfor1, sfor2, sfor3

    ranges = [(17, 28, k4, 'sfor4'), (21, 32, k1, 'sfor1'), (29, 60, k2, 'sfor2'), (49, 59, k3, 'sfor3')]
    result_printed = False

    for low, high, value, sfor_var in ranges:
        if low <= k <= high:
            globals()[sfor_var] = value
        else:
            globals()[sfor_var] = "**"
        # print(globals()[sfor_var])
        result_printed = result_printed or (low <= k <= high)

    if not result_printed:
        print("**")

screen_for_orifice_range(k, tdl_orifice_num)

def product_flow_rate(sfor):

    if sfor == "**":
        pfr = "N/A"
    else:
        pfr = tdl_num_nozzles * sfor * tdl_operating_pressure ** 0.5 / tdl_lsg ** 0.5

    return pfr

pfr1 = product_flow_rate(sfor1)
pfr2 = product_flow_rate(sfor2)
pfr3 = product_flow_rate(sfor3)
pfr4 = product_flow_rate(sfor4)

# print(pfr4, pfr1, pfr2, pfr3)

def powder_flow_rate(pfr, tdl_lsg, tdl_lpcs, tdl_ppcm):

    if pfr == "N/A":
        ans = "N/A"
    else:
        ans = pfr * tdl_lsg * tdl_lpcs/100 * (1+tdl_ppcm/100)

    return ans

powder_r1 = powder_flow_rate(pfr1, tdl_lsg, tdl_lpcs, tdl_ppcm)
powder_r2 = powder_flow_rate(pfr2, tdl_lsg, tdl_lpcs, tdl_ppcm)
powder_r3 = powder_flow_rate(pfr3, tdl_lsg, tdl_lpcs, tdl_ppcm)
powder_r4 = powder_flow_rate(pfr4, tdl_lsg, tdl_lpcs, tdl_ppcm)

swirl_number = {'SWL1':[k1, sfor1, pfr1, powder_r1],
                'SWL2':[k2, sfor2, pfr2, powder_r2],
                'SWL3':[k3, sfor3, pfr3, powder_r3],
                'SWL4':[k4, sfor4, pfr4, powder_r4]}

# print(tabulate(table_data, headers=headers, tablefmt="pretty"))
table_data = []
for key, values in swirl_number.items():
    row = [key] + values
    table_data.append(row)

headers = ["Swirl Number", "K Factor", "Screen for Orifice Range", "Product Flow Rate", "Powder Flow Rate"]

print(tabulate(table_data, headers=headers, tablefmt="pretty"))

def get_swirl_data(swirl_key):
    swirl_data = swirl_number.get(swirl_key)
    if swirl_data:
        return swirl_data
    else:
        return None

def main():
    swirl_data = get_swirl_data(swirl_input)

    if swirl_data:
        headers = ["Parameter", "Value"]
        data = [
            ["Number of Nozzles", tdl_num_nozzles],
            ["Swirl Number", swirl_input],
            ["Orifice Number", k],
            ["Operating Pressure", tdl_operating_pressure],
            ["Liquid Specific Gravity", tdl_lsg],
            ["Liquid Flow Rate", swirl_data[2]],
            ["Spray Angle at 69 bar", tdl_spa,],
            ["Liquid Percent Solids", tdl_lpcs],
            ["Powder Percent Moisture", tdl_ppcm],
            ["Powder Flow Rate", swirl_data[3]]
        ]
        print(tabulate(data, headers=headers, tablefmt="pretty"))
    else:
        print("Invalid swirl number.")

if __name__ == "__main__":
    main()
