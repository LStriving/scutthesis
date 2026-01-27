import re
import sys

def replace_inline_math(text):
    """
    Replaces $...$ with \(...\) while preserving $$...$$ and \$
    """
    # Pattern explanation:
    # 1. (\$\$[\s\S]*?\$\$) -> Matches double dollar display math (captured in group 1)
    # 2. (\\$)              -> Matches escaped dollar signs (captured in group 2)
    # 3. \$([\s\S]*?)\$     -> Matches single dollar inline math (captured content in group 3)
    
    pattern = re.compile(r'(\$\$[\s\S]*?\$\$)|(\\\$)|(?<!\\)\$(.*?)(?<!\\)\$')

    def replacement(match):
        # If Group 1 (Display Math) exists, return it unchanged
        if match.group(1):
            return match.group(1)
        
        # If Group 2 (Escaped Dollar) exists, return it unchanged
        if match.group(2):
            return match.group(2)
        
        # If we hit the third part, it's inline math. 
        # Wrap the content (group 3) with \( and \)
        return r'\(' + match.group(3) + r'\)'

    return pattern.sub(replacement, text)

# --- Main execution block ---
if __name__ == "__main__":
    # Example usage with string
    # sample_text = r"""
    # Here is an inline formula: $F^{app}_{\text{bw}}$.
    # Here is a display formula:
    # $$E = mc^2$$
    # And here is a cost: \$50.
    # Multi-line inline: $a = 
    # b + c$
    # """
    
    # print("--- Original ---")
    # print(sample_text)
    
    # converted_text = replace_inline_math(sample_text)
    
    # print("\n--- Converted ---")
    # print(converted_text)

    # UNCOMMENT THE LINES BELOW TO USE WITH A FILE
    # input_filename = 'input.tex'
    # output_filename = 'output.tex'
    # read this from args
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--output', '-o', default=None)
    args = parser.parse_args()
    input_filename = args.input
    if args.output is None:
        output_filename = input_filename
    else:
        output_filename = args.output
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = replace_inline_math(content)
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"\nSuccessfully converted {input_filename} to {output_filename}")
    except FileNotFoundError:
        print(f"Error: Could not find file {input_filename}")