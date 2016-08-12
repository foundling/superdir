def get_now():

    import datetime

    dt_now = datetime.datetime.now()
    date_string = str(dt_now) 
    date_label = date_string.split('.')[0].replace(' ','_')

    return date_label

def handle_args(args):
    ''' Args does not include the filename from sys.argv[0] '''

    output_dir = None
    schema = None
    date_stamp = 'SUPERDIR_OUTPUT_{}'.format(get_now())

    if sys.stdin.isatty():

        # cat schema.txt | superdir [ new_app ]

        if len(args) == 0:
            output_dir = date_stamp 

        elif len(args) == 1:
            output_dir = args[0]

        else: 
            usage()

        schema = list(sys.stdin)

    else:

        # superdir schema.txt [ new_app ]

        if len(args) == 1:
            output_dir = date_stamp 

        if len(args) == 2:
            output_dir = args[1]

        else:
            usage()

        with open(args[0]) as fh:
            schema = [ line for line in fh ]
        
    return schema, output_dir
