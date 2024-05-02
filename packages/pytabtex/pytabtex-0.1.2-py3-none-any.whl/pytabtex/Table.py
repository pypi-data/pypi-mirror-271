import pandas as pd

class Header:
    def __init__(self, columns, title=None) -> None:
        """
        Create an instance of the Header object.

        Parameters
        ----------
        columns : dict
            The columns of the table
            The key is the name of the column
            The value is a list of subcolumns or 0 in case of no subcolumns.

        title : str
            The title of the table
        """
        self.n_rows = self.drows(columns)
        self.n_cols = 0
        self.title = title
        self.output = self.render(columns)
        return
    
    def drows(self, columns) -> int:
        self.n_rows = 1
        for col, value in columns.items():
            if isinstance(value, list):
                self.n_rows = 2
                break
        return self.n_rows
    
    def render(self, columns) -> str:
        """
        Write latex syntax for the header of the table

        Parameters
        ----------
        columns : dict
            The columns of the table
            The key is the name of the column
            The value is a list of subcolumns or 0 in case of no subcolumns.
        
        Returns
        -------
        str
            The latex syntax for the header of the table
        """
        # Initialize variables
        index = 1
        output_1 = "\\hline\n"
        c_line = ""
        output_2 = ""
        for col, value in columns.items():
            # Case where there are subcolumns
            if isinstance(value, list):
                self.n_cols += len(value)
                output_1 += f"\\multicolumn{{{len(value)}}}{{|c|}}{{{col}}} & "
                c_line += f"\\cline{{{index}-{index+len(value)-1}}} "
                for subcol in value:
                    output_2 += subcol + " & "
                index += len(value)
            # Case where there are no subcolumns
            elif value == 0:
                self.n_cols += 1
                if self.n_rows == 1:
                    output_1 += col + " & "
                else:
                    output_1 += f"\\multirow{{{self.n_rows}}}{{*}}{{{col}}} & "
                    output_2 += " & "
                index += 1
        # add title if there is any
        if self.title:
            output_1 = (f"\\multicolumn{{{self.n_cols}}}{{|c|}}{{{self.title}}}"
            "\\\\\n" + output_1)

        output_1 = output_1[:-2] + "\\\\\n"
        c_line = c_line[:-1] + "\n"
        output_2 = output_2[:-2] + "\\\\\n"

        return output_1 + c_line + output_2 if self.n_rows == 2 else output_1
    
class Body:
    def __init__(self, body, highlight=None) -> None:
        """
        Create an instance of the Body object.
        
        Parameters
        ----------
        body : dict
            The data to add to the table
        highlight : dict
            highlight a given value in the table
            Possibles values :
                {"max" : 0} - highlight the biggest value by rows
                {"max" : 1} - highlight the biggest value by columns
                {"min" : 0} - highlight the smallest value by rows
                {"min" : 1} - highlight the smallest value by columns
        """
        self.lines = self.dlines(body)
        self.highlight = highlight
        self.output = self.render()
        return
    
    def dlines(self, body) -> dict:
        if isinstance(body, dict):
            return body
        elif isinstance(body, pd.DataFrame):
            return body.set_index(0).T.to_dict(orient='list')
        elif isinstance(body, str):
            data = pd.read_csv(body, header=None)
            return data.set_index(0).T.to_dict(orient='list')
        else:
            raise ValueError("The body must be a dictionary, a pandas DataFrame or a path to a csv file")
        
    def render(self) -> str:
        """
        Write latex syntax for the body of the table

        Parameters
        ----------
        body : dict
            The data to add to the table

        Returns
        -------
        str
            The latex syntax for the body of the table
        """
        output = "\\hline\n"
        for k, key in enumerate(self.lines.keys()):
            output += key + " & "
            for v, value in enumerate(self.lines[key]):
                if self.highlight:
                    opp = max if "max" in self.highlight else min
                    if self.highlight[opp.__name__] == 0 and\
                       value == opp(self.lines[key]):
                        output += "\\textbf{" + str(value) + "} & "
                    elif self.highlight[opp.__name__] == 1 and\
                    value == opp([self.lines[k][v] for k in self.lines.keys()]):
                        output += "\\textbf{" + str(value) + "} & "
                    else:
                        output += str(value) + " & "
                else:
                    output += str(value) + " & "
            output = output[:-2] + "\\\\\n"
        output += "\\hline\n"
        return output

class Table:
    def __init__(self, columns, body, title=None, highlight=None, caption=None,
                 orientation="P", position="htbp", align_cols="c") -> None:
        self.header = Header(columns, title)
        self.body = Body(body, highlight)
        self.position = position
        self.orientation = orientation
        self.caption = caption
        self.align_cols = align_cols
        self.output = self.render()

    def render(self) -> str:
        output = f"\\begin{{{'table' if self.orientation == 'P' else 'sidewaystable'}}}[{self.position}]\n"
        output += "\\centering\n"
        output += f"\\begin{{tabular}}{{|{(self.align_cols + '|') * self.header.n_cols}}}\n"
        output += self.header.output
        output += self.body.output
        output += "\\end{tabular}\n"
        if self.caption:
            output += f"\\caption{{{self.caption}}}\n"
        output += f"\\end{{{'table' if self.orientation == 'P' else 'sidewaystable'}}}\n"
        return output