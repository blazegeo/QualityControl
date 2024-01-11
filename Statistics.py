def EPA_conc(excel: list) -> list:
    """Grab the EPA concentration from both ILRMs if greater than 0, might need more conditions like DHA corrected or not"""
    conc = []
    for x, y in zip(excel[("ILRM 1", "EPA (mg/g)")].values,
                    excel[("ILRM 2", "EPA (mg/g)")].values):  # Using the zip function to pair the lists
        try:
            x = float(x)
            if x > 0:
                conc.append(x)
            y = float(y)
            if y > 0:
                conc.append(y)
        except ValueError:
            continue
    return conc


def EPA_percent(excel: list) -> list:
    """Grab the EPA percent from both ILRMs"""
    percent = []
    for x, y in zip(excel[("ILRM 1", "EPA (%)")].values,
                    excel[("ILRM 2", "EPA (%)")].values):  # Using the zip function to pair the lists
        try:
            x = float(x)
            if x > 0:
                percent.append(x)
            y = float(y)
            if y > 0:
                percent.append(y)
        except ValueError:
            continue
    return percent


# noinspection PyTypeChecker
def DHA_conc(excel: list) -> list:
    """Grab the DHA concentration from both ILRMs if greater than 0, might need more conditions like DHA corrected or not"""
    conc = []
    for x, y in zip(excel[("ILRM 1", "DHA (mg/g)")].values,
                    excel[("ILRM 2", "DHA (mg/g)")].values):  # Using the zip function to pair the lists
        try:
            x = float(x)
            if x > 0:
                conc.append(x)
            y = float(y)
            if y > 0:
                conc.append(y)
        except ValueError:
            continue
    return conc


def DHA_percent(excel: list) -> list:
    """Grab the DHA percent from both ILRMs"""
    percent = []
    for x, y in zip(excel[("ILRM 1", "DHA (%)")].values,
                    excel[("ILRM 2", "DHA (%)")].values):  # Using the zip function to pair the lists
        try:
            x = float(x)
            if x > 0:
                percent.append(x)
            y = float(y)
            if y > 0:
                percent.append(y)
        except ValueError:
            continue
    return percent


def GC(excel: list) -> list:
    """Grab the GC used from both ILRMS which will be the same thing twice"""
    GC = []
    c = 0
    for x in excel["", "GC"].values:
        # contingency for empty rows or single ILRM ran

        if excel["ILRM 1", "EPA (%)"][c] != "" and excel["ILRM 1", "EPA (%)"][c] != 0:
            GC.append(x)
        if excel["ILRM 2", "EPA (%)"][c] != "" and excel["ILRM 2", "EPA (%)"][c] != 0:
            GC.append(x)
        c += 1
    return GC


def Date(excel: list) -> list:
    """Grab the date twice from the sheet"""
    Date = []
    c = 0
    for x in excel.index:
        if excel["ILRM 1", "EPA (%)"][c] != "" and excel["ILRM 1", "EPA (%)"][c] != 0:
            Date.append(x)
        if excel["ILRM 2", "EPA (%)"][c] != "" and excel["ILRM 2", "EPA (%)"][c] != 0:
            Date.append(x)
        c += 1
    return Date


def Operator(excel: list) -> list:
    """Grab the operator name from both ILRMs which will be the same thing twice"""
    Oper = []
    c = 0
    for x in excel["", "Operator"].values:
        # contingency for empty rows or single ILRM ran

        if excel["ILRM 1", "EPA (%)"][c] != "" and excel["ILRM 1", "EPA (%)"][c] != 0:
            Oper.append(x)
        if excel["ILRM 2", "EPA (%)"][c] != "" and excel["ILRM 2", "EPA (%)"][c] != 0:
            Oper.append(x)
        c += 1
    return Oper


def Fat(excel: list) -> list:
    """Grab the %Fat and multiply it by 100 so its a percent"""
    Fat = []
    for x, y in zip(excel[("ILRM 1", "%fat")].values, excel[("ILRM 2", "%fat")].values):

        if x != 0 and x != "":
            x = float(x)
            x = x * 100
            Fat.append(x)

        if y != 0 and y != "":
            y = float(y)
            y = y * 100
            Fat.append(y)
    return Fat


def Diditpass(spec: list):
    """Checks whether the ILRM passed or failed returns True or False"""

    # List to return
    QC = []

    # Quality control specs
    dha_percent_low = 36.46
    dha_percent_high = 40.20
    dha_concentration_low = 331.80
    dha_concentration_high = 380.61

    epa_percent_low = 17.24
    epa_percent_high = 18.90
    epa_concentration_low = 162.09
    epa_concentration_high = 173.41
    for x in range(0, len(spec.index)):
        if (epa_percent_low < spec["EPA (%)"][x] < epa_percent_high) & \
                (epa_concentration_low < spec["EPA (mg/g)"][x] < epa_concentration_high) & \
                (dha_percent_low < spec["DHA (%)"][x] < dha_percent_high) & \
                (dha_concentration_low < spec["DHA (mg/g)"][x] < dha_concentration_high):
            QC.append("Pass")

        else:
            QC.append("Fail")
    return QC


def DHA_Corrected(excel: list) -> list:
    """Grabs whether DHA corrected"""

    Corrected = []
    c = 0
    for x in excel['', 'DHA RRF Corrected']:
        if excel["ILRM 1", "EPA (%)"][c] != "" and excel["ILRM 1", "EPA (%)"][c] != 0:
            Corrected.append(x)
        if excel["ILRM 2", "EPA (%)"][c] != "" and excel["ILRM 2", "EPA (%)"][c] != 0:
            Corrected.append(x)
        c += 1

    return Corrected


def confidence_int(df: list):
    """Finding the confidence interval for the numeric features of the dataframe at 95% confidence"""
    import math as m  # for mean and standard deviation
    import scipy.stats  # For getting the critical value such as Figure 12.3 Critical Values of T
    import statistics as stat
    columns = ["EPA (%)", "EPA (mg/g)", "DHA (%)", "DHA (mg/g)", "% Fat"]
    confidence = []
    for x in range(0, len(columns)):
        mean = stat.mean(df[(columns[x])].values)
        n = len(df[(columns[x])].values)
        dof = n - 1
        t = abs(scipy.stats.t.ppf(q=((1 - 0.95) / 2), df=dof))  # Absolute value of the 95% confidence t-value
        s = stat.stdev(df[(columns[x])].values)
        name = columns[x]
        interval = (t * s) / m.sqrt(n)
        line = "We are 95 % confident that the true answer of the <b>" + name + "</b> lies within the confidence interval at <b>" + str(
            "%.2f" % mean) + " +/- " + str("%.2f" % interval) + "</b>"
        confidence.append(line + "<br />")
    return "".join(confidence)  # returns the string


def figures_to_html(filename, values, progress_bar):
    '''Saves a list of plotly figures in an html file.

    Parameters
    ----------
    values : grabs the values from the GUI

    filename : str
        File name to save in.

    progress_bar : window element
        Bar to update while thread is running

    #https://stackoverflow.com/questions/46821554/multiple-plotly-plots-on-1-page-without-subplot
    '''
    import plotly.offline as pyo
    import io
    import time
    dashboard = io.open(filename, 'w', encoding="utf-8")
    dashboard.write("<html><head>"
                    "<title> Quality Control Analysis </title>"
                    "</head><body>" + "\n")
    # 10% done
    progress_bar.update(1)
    time.sleep(1)
    # Building Table of Contents
    dashboard.write(
        "<h1 id = 'top'> Table of Contents </h1>"
        "<ol class = 'toc' role = 'list'>"
        "<li>"
        "<a href = '#one'>"
        "<span class = 'title'> Confidence Intervals </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#two'>"
        "<span class = 'title'> Statistic Tables </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#three'>"
        "<span class = 'title'> Box Plots </span>"
        "</a>"
        "</li>"
        "<li>"
        "<a href = '#four'>"
        "<span class = 'title'> Visualization Tool </span>"
        "</a>"
        "</li>"
        "</ol>"
    )
    # Adding the confidence interval and groupby dataframes
    from Scrape import excel
    # 30% done
    progress_bar.update_bar(3)
    time.sleep(1)
    Conf_Int, DHA_Corrected, GC, Operator, QC, figs, tableau = excel(values)

    dashboard.write(
        "<a href = '#top'>"
        "<h1 id = 'one'> Confidence Intervals </h1>"
        "</a>" + str(Conf_Int)
    )
    dashboard.write(
        "<a href = '#top'>"
        "<h1 id = 'two'> Statistic Tables </h1>"
        "</a>"
    )
    dashboard.write(DHA_Corrected.to_html())
    dashboard.write(GC.to_html())
    dashboard.write(Operator.to_html())
    dashboard.write(QC.to_html())
    dashboard.write(
        "<a href = '#top'>"
        "<h1 id = 'three'> Box Plots </h1>"
        "</a>"
    )
    # 60% done
    progress_bar.update_bar(6)
    time.sleep(2)
    # Loop to add the plotly figures
    add_js = True
    for fig in figs:
        inner_html = pyo.plot(
            fig, include_plotlyjs=add_js, output_type='div'
        )

        dashboard.write(inner_html)
        add_js = False  # Saves the file from becoming bloated with javascript

    # Adding the PyGWalker (Maybe the Json/ javascript)
    dashboard.write(
        "<a href = '#top'>"
        "<h1 id = 'four'> Visualization Tool </h1>"
        "</a>"
    )

    dashboard.write(tableau)
    dashboard.write("<footer>"
        "<p> Code by Abdul Samateh </p>"
        "<p><a href = 'mailto:samateh1@umbc.edu'> samateh1@umbc.edu </a></p> "
                    "</footer>")
    # Closing the html
    dashboard.write("</body></html>" + "\n")
    # 80% done
    progress_bar.update_bar(8)
    time.sleep(1)


def show_in_window(values):
    """Will be used to display the html page in its own pop up and not in browser!"""
    import sys, os
    import plotly.offline
    from PyQt6.QtCore import QUrl
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    web = QWebEngineView()
    file_path = os.path.abspath(os.path.join(os.path.dirname(values["-FILE-"]), values[0] + ".html"))
    web.load(QUrl.fromLocalFile(file_path))
    web.show()
    sys.exit(app.exec())
