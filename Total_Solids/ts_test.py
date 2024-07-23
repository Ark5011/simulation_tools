fat_content = int(input("Fat Content: "))
start_density = int(input("Density: "))

for i in range(61):
    current_density = start_density + i
    total_solids = (138.2 - (136.206 / current_density * 1000)) / (0.505 - (0.00651101 * fat_content))
    print(f"{current_density:.2f}\t{total_solids:.2f}")
