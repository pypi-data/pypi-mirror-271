import os
import subprocess
import shlex
import json
import jsonargparse

def setup_parser():
    
    parser = jsonargparse.ArgumentParser(
        description="A command line tool for generating templated documentation from clis",
    )
    parser.add_argument(
        "--input", type=str, default="templated.md", help="The input template file",)
    parser.add_argument(
        "--output", type=str, default="output.md", help="The output file",)
    
    return parser
    

def verify_args(dargs):
    # Check if input file exists
    if not os.path.exists(dargs["input"]):
        print(f"Error: Input file {dargs['input']} does not exist.")
        return False
    return True

def run_cli(parser):
    args = parser.parse_args()
    dargs = jsonargparse.namespace_to_dict(args)
    if verify_args(dargs):
        create_doc(dargs)
    else:
        exit(1)

def create_doc(dargs):
    # Read input file to string
    template_filename = dargs["input"]
    output_filename = dargs["output"]
    same_file = False
    if template_filename == output_filename:
        same_file = True
        orig_output_filename = output_filename
        output_filename = f"tmp-{output_filename}"
    with open(template_filename, "r") as f:
        template = f.read()

    o = open(output_filename, "w")

    # Scan through the file and run the commands
    l = template.split("<!--")
    o.write(l[0])
    if len(l) == 1:
        print(f"No commands found in template {template_filename}")
        return

    for section in l[1:]:
        sectionl = section.split("-->")
        if len(sectionl) != 2:
            print(f"Error: Command section not properly enclosed, in section: {section}")
            exit(1)
        command = sectionl[0].strip()
        tail = sectionl[1]
        try:
            command_obj = json.loads(command)
        except json.JSONDecodeError as e:
            print(f"Error: Command section not valid json, in section: {section}")
            exit(1)
        object_type = command_obj.get("object-type", "command")

        if object_type == "command":
            remove_previous = False
            skip = command_obj.get("skip", False)
            if skip:
                o.write(f'<!--\n{command}\n-->\n')
                continue

            output = run_command(command_obj)
            # Handle printing:
            # Retain original object in order to allow for re runs and debugging:
            o.write(f'<!--\n{command}\n-->\n') 
            o.write('<!-- { "object-type": "command-output-start" } -->\n')
            if command_obj.get("print_command", False):
                o.write(f"```bash\n{command_obj['command']}\n```\n")
            format = command_obj.get("output-format", 'bash')
            limit = command_obj.get("limit", 0)
            if limit > 0:
                output = '\n'.join(output.split('\n')[:limit]) + '\n'
            o.write(f"```{format}\n{output}```\n")
            o.write('<!-- { "object-type": "command-output-end" } -->\n')
            o.write(tail)
            remove_previous = True
        elif object_type == "command-output-start":
            if remove_previous:
                continue
            else:
                o.write(f'<!--{command}-->')
                tail = tail.lstrip()
                o.write(f"\n{tail}")
        elif object_type == "command-output-end":
            if remove_previous:
                remove_previous = False
                tail = tail.lstrip()
                o.write(f"\n{tail}")
                continue
            else:
                o.write(f'<!--{command}-->')
                tail = tail.lstrip()
                o.write(f"\n{tail}")

    o.close()
    if same_file:
        os.rename(output_filename, orig_output_filename)     




def is_mapping_string(typeclass, value):
    # TODO: add more validations
    if len(value.split("::")) != 2 :
        return True
    return False

def run_command(command_obj):
    stdout = run_command_with_env(command_obj)
    return stdout

def run_command_with_env(command_obj):
    command = command_obj["command"]
    # Split the command into words
    parts = shlex.split(command)
    
    # Replace capitalized words with environment variables if they exist in the environment
    updated_parts = []
    for part in parts:
        if part.isupper() and part in os.environ:
            updated_parts.append(os.environ[part])
        else:
            updated_parts.append(part)
    
    # Join the command back together and run it
    final_command = ' '.join(updated_parts)
    try:
        # Execute the command and capture the output
        result = subprocess.run(final_command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Handle errors in subprocess execution
        error_strat = command_obj.get("error-strategy", "ignore")
        if error_strat == "exit":
            print(f"Error: {e}\n{e.stderr}")
            exit(1)
        elif error_strat == "ignore":
            return e.stderr
        else:
            print(f"Error: Invalid error strategy {error_strat}")
            exit(1)

def main():
    parser = setup_parser()
    run_cli(parser)

# Example usage
if __name__ == "__main__":
    main()


