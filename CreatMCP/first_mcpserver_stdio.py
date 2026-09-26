from fastmcp import FastMCP

mcp = FastMCP()

@mcp.tool()
def fetch():
    ''' use this tool to fetch data from a source.'''

    return {"data": "Hello mcp"} 

@mcp.tool()
def process(path:str):

    return{"processed_data": "data has been processed! at path" + path}

if __name__ == "__main__":

    mcp.run(transport = "stdio")