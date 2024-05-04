from .handle import Handle


class HandleInfo(Handle):
    def response(self) -> str:
        from ..html.core import Document
        doc = Document()

        def output_parameters(parameters: dict):
            table = doc.html.body.create.component.table()
            if len(parameters) > 0:
                for ki, vi in parameters.items():
                    row = table.body.add_row()
                    row.add_cell(ki)
                    row.add_cell(vi)

        output_parameters(self.requests.cookies)
        output_parameters(self.requests.gets)
        output_parameters(self.requests.posts)
        output_parameters(self.requests.headers)
        return doc.output()
