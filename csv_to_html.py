import csv
import configparser
import os

class CSVToHTML:
    def __init__(self, csv_name, output_html):
        self.csv_name = csv_name
        self.output_html = output_html
        self.data = []
    
    def read_csv(self):
        if os.path.isfile(self.csv_name) and os.path.getsize(self.csv_name) > 0:
            with open(self.csv_name, encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.data.append(row)
        else:
            print("Error: Invalid file or file is empty.")

    def generate_html(self):
            html = '''
                <html>
                    <head>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
                        <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.1/css/jquery.dataTables.min.css">
                        <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
                        <script src="https://cdn.datatables.net/1.13.1/js/jquery.dataTables.min.js"></script>
                        <style>

                            /* Add css for filtering */
                            .dataTables_filter {
                                margin-top: 25px;
                            }
                        </style>
                        <script>
                            $(document).ready(function () {
                                var table = $('#example').DataTable();
                            
                                $('#example tbody').on('click', 'tr', function () {
                                    $(this).toggleClass('selected');
                                });
                            
                                $('#button').click(function () {
                                    alert(table.rows('.selected').data().length + ' row(s) selected');
                                });
                            });
                        </script>
                    </head>
                    <body>
                        <button id="button">Row count</button>
                        <table class="example" class="display" style="width:100%">
                            <thead>
                                <tr>
                                    <th>handle</th>
                                    <th>content</th>
                                    <th>url</th>
                                    <th>tweet</th>
                                </tr>
                            </thead>                      
                            <tbody>
            '''
            for row in self.data:
                html += '''
                    <tr>
                        <td>{}</td>
                        <td>{}</td>
                        <td><a href="{}" target="_blank">{}</a></td>
                        <td><a href="{}" target="_blank">{}</a></td>
                    </tr>
                '''.format(row['handle'], row['content'], row['url'], row['url'], row['tweet'], row['tweet'])
            html += '''
                            </tbody>
                            <tfoot>
                                <tr>
                                    <th>handle</th>
                                    <th>content</th>
                                    <th>url</th>
                                    <th>tweet</th>
                                </tr>
                            </tfoot>                               
                        </table>
                    </body>
                </html>
            '''
            with open(self.output_html, "w") as file:
                file.write(html)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    csv_name = config['DEFAULT']['tweet_file']
    output_html = config['DEFAULT']['output_html']
    if csv_name:
        csv_to_html = CSVToHTML(csv_name, output_html)
        csv_to_html.read_csv()
        csv_to_html.generate_html()
    else:
        print("Error: tweet_file not found in config.ini")
