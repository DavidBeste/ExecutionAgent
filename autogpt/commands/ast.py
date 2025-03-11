import clang.cindex

clang.cindex.Config.set_library_file("/usr/lib/x86_64-linux-gnu/libclang-20.so")  # Set the path to libclang.so

def extract_function_heads(code: str):
    """
    Extracts all function headers from a given C code string.
    """
    index = clang.cindex.Index.create()
    translation_unit = index.parse('tmp.c', args=['-xc'], unsaved_files=[('tmp.c', code)], options=0)
    
    function_heads = []
    
    for cursor in translation_unit.cursor.get_children():
        if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL and cursor.location.file and cursor.location.file.name == 'tmp.c':
            # Extract return type
            return_type = cursor.result_type.spelling
            
            # Extract function name
            function_name = cursor.spelling
            
            # Extract parameters
            params = [
                f"{param.type.spelling} {param.spelling}" for param in cursor.get_arguments()
            ]
            
            function_head = f"{return_type} {function_name}({', '.join(params)})"
            function_heads.append(function_head)
    
    return function_heads

def extract_function_heads_from_file(file_path: str):
    """
    Extracts all function headers from a C file without using unsaved files.
    """
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path, args=['-xc'])
    
    function_heads = []
    
    for cursor in translation_unit.cursor.get_children():
        if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL and cursor.location.file and cursor.location.file.name == file_path:
            # Extract return type
            return_type = cursor.result_type.spelling
            
            # Extract function name
            function_name = cursor.spelling
            
            # Extract parameters
            params = [
                f"{param.type.spelling} {param.spelling}" for param in cursor.get_arguments()
            ]
            
            function_head = f"{return_type} {function_name}({', '.join(params)})"
            function_heads.append(function_head)
    
    return function_heads

def extract_function_body(code: str, function_head: str):
    """
    Extracts the function body given a function header from the provided C code string.
    """
    index = clang.cindex.Index.create()
    translation_unit = index.parse('tmp.c', args=['-xc'], unsaved_files=[('tmp.c', code)], options=0)
    
    for cursor in translation_unit.cursor.get_children():
        if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL and cursor.location.file and cursor.location.file.name == 'tmp.c':
            extracted_head = f"{cursor.result_type.spelling} {cursor.spelling}({', '.join([param.type.spelling + ' ' + param.spelling for param in cursor.get_arguments()])})"
            if extracted_head == function_head:
                return code[cursor.extent.start.offset:cursor.extent.end.offset]
    
    return None

def extract_function_body_from_file(file_path: str, function_head: str):
    """
    Extracts the function body given a function header from a C file without using unsaved files.
    """
    index = clang.cindex.Index.create()
    translation_unit = index.parse(file_path, args=['-xc'])
    
    with open(file_path, 'r') as f:
        code = f.read()
    
    for cursor in translation_unit.cursor.get_children():
        if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL and cursor.location.file and cursor.location.file.name == file_path:
            extracted_head = f"{cursor.result_type.spelling} {cursor.spelling}({', '.join([param.type.spelling + ' ' + param.spelling for param in cursor.get_arguments()])})"
            if extracted_head == function_head:
                return code[cursor.extent.start.offset:cursor.extent.end.offset]
    
    return None

# Example usage
if __name__ == "__main__":
    c_code = """
    int add(int a, int b) {
        return a + b;
    }
    
    void print_hello() {
        printf("Hello, World!\n");
    }
    """
    
    headers = extract_function_heads(c_code)
    for header in headers:
        print(header)
    
    # Example usage for file-based extraction
    file_headers = extract_function_heads_from_file("../../execution_agent_workspace/libtiff/libtiff/tif_read.c")
    for header in file_headers:
        print(header)
    
    # Example usage for extracting a function body
    function_body = extract_function_body(c_code, "int add(int a, int b)")
    print(function_body)
    
    function_body_from_file = extract_function_body_from_file("../../execution_agent_workspace/libtiff/libtiff/tif_read.c", "tmsize_t _TIFFReadEncodedTileAndAllocBuffer(TIFF * tif, uint32_t tile, void ** buf, tmsize_t bufsizetoalloc, tmsize_t size_to_read)")
    print(function_body_from_file)
