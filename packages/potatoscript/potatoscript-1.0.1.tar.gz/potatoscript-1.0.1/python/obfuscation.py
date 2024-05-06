import py_compile
import marshal

# Step 1: Compile Python code to bytecode
with open('potato.py', 'rb') as f:
    compiled_code = compile(f.read(), 'potato.py', 'exec')

# Step 2: Obfuscate the bytecode
obfuscated_code = marshal.dumps(compiled_code)

# Step 3: Save the obfuscated bytecode to a file
with open('potato.pyc', 'wb') as f:
    f.write(obfuscated_code)
