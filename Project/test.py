from taint import TaintAnalyzer

# Create a TaintAnalyzer object
analyzer = TaintAnalyzer()

# Run the taint analysis on a script
with open('main.py', 'r') as f:
    script = f.read()
    results = analyzer.analyze(script)

# Print the results
print(results)
