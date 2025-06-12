import re
import matplotlib.pyplot as plt

# Initialize storage for residuals
iterations = []  # Store iteration numbers
residuals = {"Ux": [], "Uy": [], "Uz": [], "p": [], "epsilon": [], "k": []}

# Regular expressions to match lines with residual data and iteration numbers
residual_pattern = re.compile(r"Solving for (\w+), Initial residual = ([\d.e+-]+), Final residual = ([\d.e+-]+)")
iteration_pattern = re.compile(r"Time = ([\d.e+-]+)")  # Adjust this based on your log format

current_iteration = 0

# Path to your log file (replace with the actual path of your log file)
log_file_path = "log.simpleFoam"  # <-- Replace this with the actual file path

# Process the log content to extract residuals and iterations
with open(log_file_path, "r") as log_file:
    for line in log_file:
        # Check for iteration information (you may need to adjust the pattern)
        iteration_match = iteration_pattern.search(line)
        if iteration_match:
            current_iteration += 1  # Increment the iteration count
            iterations.append(current_iteration)

        # Check for residual data
        residual_match = residual_pattern.search(line)
        if residual_match:
            field = residual_match.group(1)
            initial_residual = float(residual_match.group(2))
            if field in residuals:
                residuals[field].append(initial_residual)

# Plot the residuals
plt.figure(figsize=(10, 6))
for field, data in residuals.items():
    if data:  # Only plot if data exists for the field
        plt.semilogy(iterations[:len(data)], data, label=f"{field} residual")

plt.xlabel("Iterations")
plt.ylabel("Residuals (log scale)")
plt.title("Residuals vs Iterations")
plt.legend()
plt.grid(True, which="both", linestyle="--", linewidth=0.5)

plt.savefig("residuals_plot.png")

plt.show()

