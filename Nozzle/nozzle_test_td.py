from tabulate import tabulate

td_num_nozzles = int(input("Number of Nozzles: "))
swirl_input = input("Enter swirl number (e.g., SW1, SW2, etc.): ")
k = float(input("Orifice Number: "))

td_orifice_num = [34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 62, 64, 66, 67, 68, 70, 73, 75,
                  76, 80, 82, 85, 86, 88, 90, 91, 94, 97, 100, 103, 106, 109, 112, 115, 118,
                  121, 127, 133, 136, 142, 145, 148, 151, 154, 157]

td_operating_pressure = float(input("Operating Pressure: "))
td_lsg = float(input("Liquid Specific Gravity: "))
td_lpcs = float(input("Liquid Per Cent Solids: "))
td_ppcm = float(input("Powder Per Cent Moisture: "))

def k_factor(k, td_orifice_num, x, y, z):

    for n in td_orifice_num:
        if n == k:
            return x * n ** 2 + y * n - z

k1 = 0.19 * k + 2.09
k2 = 0.38 * k - 3.8
k3 = k_factor(k, td_orifice_num, -0.000698, 0.513778, 5.602094)
k4 = k_factor(k, td_orifice_num, 0.00187, 0.32312, -0.68223)
k5 = k_factor(k, td_orifice_num, 0.0002403, 0.6758402, 7.503516)
k6 = k_factor(k, td_orifice_num, 0.001007, 0.812664, 11.694463)
k7 = k_factor(k, td_orifice_num, 0.000865, 1.128301, 21.295354)
k8 = k_factor(k, td_orifice_num, 0.0014, 1.4509, 34.78843)
k9 = k_factor(k, td_orifice_num, 0.0029, 1.5332, 34.527)
k10 = k_factor(k, td_orifice_num, 0.00162, 2.16933, 62.616)

# print(k1, k2, k3, k4, k5, k6, k7, k8, k9, k10)

sfor1, sfor2, sfor3, sfor4, sfor5, sfor6, sfor7, sfor8, sfor9, sfor10= None,None,None,None,None,None,None,None,None,None

def screen_for_orifice_range(k, td_orifice_num):
    global sfor1, sfor2, sfor3, sfor4, sfor5, sfor6, sfor7, sfor8, sfor9, sfor10

    ranges = [(34, 60, k1, 'sfor1'), (34, 82, k2, 'sfor2'), (34, 105, k3, 'sfor3'), (34, 137, k4, 'sfor4'),
              (34, 145, k5, 'sfor5'), (35, 153, k6, 'sfor6'), (37, 153, k7, 'sfor7'), (48, 160, k8, 'sfor8'),
              (76, 160, k9, 'sfor9'), (84, 160, k10, 'sfor10')]
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

screen_for_orifice_range(k, td_orifice_num)

def product_flow_rate(sfor):

    if sfor == "**":
        pfr = "N/A"
    else:
        pfr = td_num_nozzles * sfor * td_operating_pressure ** 0.5 / td_lsg ** 0.5

    return pfr

pfr1 = product_flow_rate(sfor1)
pfr2 = product_flow_rate(sfor2)
pfr3 = product_flow_rate(sfor3)
pfr4 = product_flow_rate(sfor4)
pfr5 = product_flow_rate(sfor5)
pfr6 = product_flow_rate(sfor6)
pfr7 = product_flow_rate(sfor7)
pfr8 = product_flow_rate(sfor8)
pfr9 = product_flow_rate(sfor9)
pfr10 = product_flow_rate(sfor10)

# print(pfr1, pfr2, pfr3, pfr4, pfr5, pfr6, pfr7, pfr8, pfr9, pfr10)

def flowrate(pfr):

    if pfr == "N/A":
        fr = "N/A"
    else:
        fr = pfr / td_num_nozzles * (69/td_operating_pressure) ** 0.5

    return fr

fr1 = flowrate(pfr1)
fr2 = flowrate(pfr2)
fr3 = flowrate(pfr3)
fr4 = flowrate(pfr4)
fr5 = flowrate(pfr5)
fr6 = flowrate(pfr6)
fr7 = flowrate(pfr7)
fr8 = flowrate(pfr8)
fr9 = flowrate(pfr9)
fr10 = flowrate(pfr10)

# print(fr1, fr2, fr3, fr4, fr5, fr6, fr7, fr8, fr9, fr10)

def spray_angle_1(pfr, fr, x):
    if pfr == "N/A":
        spa_1 = "N/A"
    else:
        spa_1 = 0.2641 * fr + x

    return spa_1

def spray_angle_2(pfr, x, fr, y, z):

    if pfr == "N/A":
        spa_2 = "N/A"
    else:
        spa_2= x * fr ** 2 + y * fr + z

    return spa_2

spa1 = spray_angle_1(pfr1, fr1, 60)
spa2 = spray_angle_1(pfr2, fr2, 50)
spa3 = spray_angle_2(pfr3, -0.000284, fr3, 0.187738, 52.394181)
spa4 = spray_angle_2(pfr4, -0.000263, fr4, 0.202401, 41.325448)
spa5 = spray_angle_2(pfr5, -0.000129, fr5, 0.14995, 35.403449)
spa6 = spray_angle_2(pfr6, -0.0000376, fr6, 0.0794284, 37.8196606)
spa7 = spray_angle_2(pfr7, -0.0000173, fr7, 0.0529205, 35.5265553)
spa8 = spray_angle_2(pfr8, -0.00000774, fr8, 0.03764802, 30.23508882)
spa9 = spray_angle_2(pfr9, -0.000000423, fr9, 0.015491835, 36.120970302)
spa10 = spray_angle_2(pfr10, -0.000000776, fr10, 0.014430671, 31.053166908)

# print(spa1, spa2, spa3, spa4, spa5, spa6, spa7, spa8, spa9, spa10)

def dropsize(spa, x, y, z):

    if spa == "N/A":
        ds = "N/A"
    else:
        ds = x * (td_operating_pressure * 14.5) ** y * (k/1000) ** z

    return ds

ds1 = dropsize(spa1, 618.3, -0.3102, 0.0627)
ds2 = dropsize(spa2, 1685.4, -0.3196, 0.3708)
ds3 = dropsize(spa3, 1020.1, -0.3484, 0.1493)
ds4 = dropsize(spa4, 727.6, -0.2587, 0.2122)
ds5 = dropsize(spa5, 837.3, -0.1845, 0.473)
ds6 = dropsize(spa6, 618.3, -0.3102, 0.0627)
ds7 = dropsize(spa7, 92.25, 0.006148, 0.132)
ds8 = dropsize(spa8, 535.5, -0.2293, 0.1268)
ds9 = dropsize(spa9, 530.6, -0.1126, 0.4453)
ds10 = dropsize(spa10, 618.3, -0.3102, 0.0627)

# print(ds1, ds2, ds3, ds4, ds5, ds6, ds7, ds8, ds9, ds10)

def powder_flow_rate(pfr, td_lsg, td_lpcs, td_ppcm):

    if pfr == "N/A":
        ans = "N/A"
    else:
        ans = pfr * td_lsg * td_lpcs/100 * (1+td_ppcm/100)

    return ans

powder_r1 = powder_flow_rate(pfr1, td_lsg, td_lpcs, td_ppcm)
powder_r2 = powder_flow_rate(pfr2, td_lsg, td_lpcs, td_ppcm)
powder_r3 = powder_flow_rate(pfr3, td_lsg, td_lpcs, td_ppcm)
powder_r4 = powder_flow_rate(pfr4, td_lsg, td_lpcs, td_ppcm)
powder_r5 = powder_flow_rate(pfr5, td_lsg, td_lpcs, td_ppcm)
powder_r6 = powder_flow_rate(pfr6, td_lsg, td_lpcs, td_ppcm)
powder_r7 = powder_flow_rate(pfr7, td_lsg, td_lpcs, td_ppcm)
powder_r8 = powder_flow_rate(pfr8, td_lsg, td_lpcs, td_ppcm)
powder_r9 = powder_flow_rate(pfr9, td_lsg, td_lpcs, td_ppcm)
powder_r10 = powder_flow_rate(pfr10, td_lsg, td_lpcs, td_ppcm)


# print(powder_flow_rate(pfr9, td_lsg, td_lpcs, td_ppcm))

swirl_number = {'SW1':[k1, sfor1, pfr1, fr1, spa1, ds1, powder_r1],
                'SW2':[k2, sfor2, pfr2, fr2, spa2, ds2, powder_r2],
                'SW3':[k3, sfor3, pfr3, fr3, spa3, ds3, powder_r3],
                'SW4':[k4, sfor4, pfr4, fr4, spa4, ds4, powder_r4],
                'SW5':[k5, sfor5, pfr5, fr5, spa5, ds5, powder_r5],
                'SW6':[k6, sfor6, pfr6, fr6, spa6, ds6, powder_r6],
                'SW7':[k7, sfor7, pfr7, fr7, spa7, ds7, powder_r7],
                'SW8':[k8, sfor8, pfr8, fr8, spa8, ds8, powder_r8],
                'SW9':[k9, sfor9, pfr9, fr9, spa9, ds9, powder_r9],
                'SW10':[k10, sfor10, pfr10, fr10, spa10, ds10, powder_r10]}

table_data = []
for key, values in swirl_number.items():
    row = [key] + values
    table_data.append(row)

headers = ["Swirl Number", "K Factor", "Screen for Orifice Range", "Product Flow Rate",
           "FloW Rate at 1000 psi", "Spray Angle at 1000 psi", "Dropsize", "Powder Flow Rate"]

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
            ["Number of Nozzles", td_num_nozzles],
            ["Swirl Number", swirl_input],
            ["Orifice Number", k],
            ["Operating Pressure", td_operating_pressure],
            ["Liquid Specific Gravity", td_lsg],
            ["Liquid Flow Rate", swirl_data[2]],
            ["Spray Angle at 69 bar", swirl_data[4]],
            ["Droplet Size (Sauter Mean)", swirl_data[5]],
            ["Liquid Percent Solids", td_lpcs],
            ["Powder Percent Moisture", td_ppcm],
            ["Powder Flow Rate", swirl_data[6]]
        ]
        print(tabulate(data, headers=headers, tablefmt="pretty"))
    else:
        print("Invalid swirl number.")

if __name__ == "__main__":
    main()
