from ArchFlowJavaWeb import ArchFlowJavaWeb
from pathlib import Path

directory_template = Path('templates/')

arch = ArchFlowJavaWeb()
arch.DirectoryExplorer.directory_template = directory_template

if __name__ == "__main__":
    args = arch.handle_args()
    arch.handler_functions_flow_java(args)
