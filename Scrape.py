# https://docs.kanaries.net/pygwalker Url for FAME MASTER SHEET:
# Decided to just grab it from local computer, if the file is uploaded and is atuosaving then the program will run the read with threading
# Will build without threading first
# https://www.geeksforgeeks.org/display-the-pandas-dataframe-in-table-style/

import Statistics as st

def excel(values) -> list:
    '''Creating the excel sheet from the input from the GUI'''
    import pandas as pd
    import datetime
    pd.set_option('display.precision', 4) # set sig fig to 4
    # Reads the Excel file just for the date index so I can use it when assigning the excel with skiprow and the function above
    dates = pd.read_excel(values["-FILE-"],
                          sheet_name="QC Tracking 2023", ##ONLY LINE TO UPDATE IF NEW SHEET##
                          header=[1],
                          index_col=0)

    # Counts number of rows I want to use in the excel
    numofrows = 1
    for x in range(0,len(dates.index) - 1):
        try:
            if dates.index.values[x] > datetime.datetime(2023, 1, 1, 0, 0):
                numofrows += 1
        except TypeError:
            continue


    excel = pd.read_excel(
        values["-FILE-"],
        sheet_name="QC Tracking 2023",
        header=[0, 1], keep_default_na=False,
        index_col=0,
        nrows=numofrows)  # change this to a lower number if it stops working or change keep_default_na to True

    dict = {'Unnamed: 0_level_0': "",
            'Unnamed: 1_level_0': "",
            'Unnamed: 2_level_0': "",
            'Unnamed: 3_level_0': "",
            'Unnamed: 4_level_0': "",
            'Unnamed: 5_level_0': "",
            'Unnamed: 6_level_0': "",
            'Unnamed: 7_level_0': "",
            'Unnamed: 8_level_0': "",
            'Unnamed: 9_level_0': "",
            "EPA AVG" : "",
            "Unnamed: 39_level_1": "EPA AVG",
            "DHA AVG" : "",
            "Unnamed: 40_level_1": "DHA AVG",
            "Unnamed: 41_level_1": "Comments"
    }
    excel.rename(columns=dict,inplace = True)

    spec = pd.DataFrame()

    spec["Date"] = st.Date(excel)
    spec["EPA (%)"] = st.EPA_percent(excel)
    spec["EPA (mg/g)"] = st.EPA_conc(excel)
    spec["DHA (%)"] = st.DHA_percent(excel)
    spec["DHA (mg/g)"] = st.DHA_conc(excel)
    spec["GC"] = st.GC(excel)
    spec["Operator"] = st.Operator(excel)
    spec["% Fat"] = st.Fat(excel)
    spec["DHA Corrected"] = st.DHA_Corrected(excel)
    spec["QC"] = st.Diditpass(spec)

    Conf_Int = st.confidence_int(spec)

    # Grouped by DHA Corrected
    DHA_Corrected = spec.drop("Date", axis=1).drop("QC", axis=1).drop("GC", axis=1).drop("Operator", axis=1).groupby(
        ["DHA Corrected"]) \
        .agg(["mean", "std", "var"])

    # Groupped by GC
    GC = spec.drop('Operator', axis=1).drop("QC", axis=1) \
        .drop("Date", axis=1).groupby(["GC", "DHA Corrected"]).agg(['mean', 'std'])

    # Grouped by Operator
    Operator = spec.drop('GC', axis=1).drop('DHA Corrected', axis=1).drop("QC", axis=1).drop("Date", axis=1).groupby(
        ["Operator"]).agg(['mean', 'std', 'var'])

    # Grouped by QC
    QC = spec.drop('Date', axis=1).drop('GC', axis=1).drop('DHA Corrected', axis=1).groupby(["QC", "Operator"]).agg(
        ["mean", "median"])

    #######Box Plots

    import pygwalker as pyg
    import plotly.express as px
    import plotly.io as pio

    pio.templates.default = "plotly_dark"

    EPA_percent_by_GC = px.box(spec, x="GC", y="EPA (%)", points="all", color="DHA Corrected",
                               hover_data=["% Fat", "DHA Corrected"],
                               title="EPA Percent by GC", color_discrete_sequence=["maroon", "green"], width=1500,
                               height=900)

    EPA_percent_by_Operator = px.box(spec, x="Operator", y="EPA (%)", points="all", color="QC",
                                     hover_data=["% Fat", "DHA Corrected"],
                                     title="EPA Percent by Operator", color_discrete_sequence=["maroon", "green"],
                                     width=1500, height=900)

    EPA_conc_by_GC = px.box(spec, x="GC", y="EPA (mg/g)", points="all", color="QC",
                            hover_data=["% Fat", "DHA Corrected"],
                            title="EPA Concentration by GC", color_discrete_sequence=["maroon", "green"], width=1500,
                            height=900)

    EPA_conc_by_Operator = px.box(spec, x="Operator", y="EPA (mg/g)", points="all", color="QC",
                                  hover_data=["% Fat", "DHA Corrected"],
                                  title="EPA Concentration by Operator", color_discrete_sequence=["maroon", "green"],
                                  width=1500, height=900)
    #######################################################
    DHA_percent_by_GC = px.box(spec, x="GC", y="DHA (%)", points="all", color="QC",
                               hover_data=["% Fat", "DHA Corrected"],
                               title="DHA Percent by GC", color_discrete_sequence=["maroon", "green"], width=1500,
                               height=900)

    DHA_percent_by_Operator = px.box(spec, x="Operator", y="DHA (%)", points="all", color="QC",
                                     hover_data=["% Fat", "DHA Corrected"],
                                     title="DHA Percent by Operator", color_discrete_sequence=["maroon", "green"],
                                     width=1500, height=900)

    DHA_conc_by_GC = px.box(spec, x="GC", y="DHA (mg/g)", points="all", color="QC",
                            hover_data=["% Fat", "DHA Corrected"],
                            title="DHA Concentration by GC", color_discrete_sequence=["maroon", "green"], width=1500,
                            height=900)

    DHA_conc_by_Operator = px.box(spec, x="Operator", y="DHA (mg/g)", points="all", color="QC",
                                  hover_data=["% Fat", "DHA Corrected"],
                                  title="DHA Concentration by Operator", color_discrete_sequence=["maroon", "green"],
                                  width=1500, height=900)
    ###########################################################
    # All of the Box Plots
    figs = [EPA_percent_by_GC, EPA_percent_by_Operator, EPA_conc_by_GC, EPA_conc_by_Operator,
            DHA_percent_by_GC, DHA_percent_by_Operator, DHA_conc_by_GC, DHA_conc_by_Operator]

    ##############################
    # Adding PyGWalker Visualizations
    vis_spec = """{"config":[{"config":{"defaultAggregated":true,"geoms":["point"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_TJ4a","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_jwTh","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_oPlb","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"},{"fid":"Date","name":"Date","semanticType":"temporal","analyticType":"dimension","basename":"Date","dragId":"GW_3S1cun0H"},{"fid":"DHA Corrected","name":"DHA Corrected","semanticType":"nominal","analyticType":"dimension","basename":"DHA Corrected","dragId":"GW_eGIacgCF"}],"measures":[{"dragId":"gw_BigQ","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_FZQR","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_xmvu","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_OeaN","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_ffGz","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_FEJ9","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"columns":[{"dragId":"gw__9mU","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_CJGY","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"}],"color":[{"dragId":"gw_Coe_","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"auto","width":320,"height":200},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_tbi0","name":"Number of Pass/ Fails by Operator and GC"},{"config":{"defaultAggregated":true,"geoms":["bar"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_nPjJ","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_yPrk","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_9JsS","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"},{"fid":"Date","name":"Date","semanticType":"temporal","analyticType":"dimension","basename":"Date","dragId":"GW_StxPI1iD"},{"fid":"DHA Corrected","name":"DHA Corrected","semanticType":"nominal","analyticType":"dimension","basename":"DHA Corrected","dragId":"GW_3HaRKNMD"}],"measures":[{"dragId":"gw_qeOD","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_ODsA","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_yzHC","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_1EVA","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_Lob3","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_9G0l","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension","sort":"ascending"}],"columns":[{"dragId":"gw_FOUX","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"mean"},{"dragId":"gw_822d","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"mean"},{"dragId":"gw_WDGI","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"mean"},{"dragId":"gw_8qcp","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"mean"}],"color":[{"dragId":"gw_H-PL","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[{"dragId":"gw_-36z","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"fixed","width":865,"height":276},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_jtW5","name":"Mean GC Performance"},{"config":{"defaultAggregated":true,"geoms":["auto"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_LiDd","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_nEa7","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_y7gV","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"},{"fid":"Date","name":"Date","semanticType":"temporal","analyticType":"dimension","basename":"Date","dragId":"GW_8N07Fa6S"},{"fid":"DHA Corrected","name":"DHA Corrected","semanticType":"nominal","analyticType":"dimension","basename":"DHA Corrected","dragId":"GW_UiQVq93r"}],"measures":[{"dragId":"gw_bsQa","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_gJJE","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_Kuty","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_V0qo","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_kbUb","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_2KUw","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"variance"}],"columns":[{"dragId":"gw_Q175","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"}],"color":[{"dragId":"gw_CCV_","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[{"dragId":"gw_bkp1","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"fixed","width":467,"height":273},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_y3RN","name":"Variance of Fat%"},{"config":{"defaultAggregated":true,"geoms":["area"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_Jja4","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_0VSH","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_qUny","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"},{"fid":"Date","name":"Date","semanticType":"temporal","analyticType":"dimension","basename":"Date","dragId":"GW_4i3XJYzs"},{"fid":"DHA Corrected","name":"DHA Corrected","semanticType":"nominal","analyticType":"dimension","basename":"DHA Corrected","dragId":"GW_wSILshB4"}],"measures":[{"dragId":"gw_mlc5","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_ad3k","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_2z6p","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_qrR7","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_sBod","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_Q3Sc","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"stdev"},{"dragId":"gw_nKFq","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"stdev"},{"dragId":"gw_gwi8","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"stdev"},{"dragId":"gw_0bWu","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"stdev"}],"columns":[{"dragId":"gw_BVoM","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"}],"color":[{"dragId":"gw_j5oS","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"auto","width":320,"height":200},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_V0Kw","name":"Std. Dev by Operator"},{"config":{"defaultAggregated":false,"geoms":["point"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_vAde","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_YiSH","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_81jl","fid":"Date","name":"Date","basename":"Date","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_gX3T","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"},{"fid":"DHA Corrected","name":"DHA Corrected","semanticType":"nominal","analyticType":"dimension","basename":"DHA Corrected","dragId":"GW_Vpkr2W8N"}],"measures":[{"dragId":"gw_Y-M0","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_ytEu","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_LfdT","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw__P7-","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_b5dX","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_iAwy","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"columns":[{"dragId":"gw_1eqS","fid":"Date","name":"Date","basename":"Date","semanticType":"temporal","analyticType":"dimension"}],"color":[{"dragId":"gw_tCJD","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"}],"opacity":[],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[{"dragId":"gw_YmCg","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"}],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"fixed","width":490,"height":360},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false},"scaleIncludeUnmatchedChoropleth":false,"colorPalette":"","useSvg":false,"scale":{"opacity":{},"size":{"domainMax":45}}},"visId":"gw_usfB","name":"% Fat over Time"},{"config":{"defaultAggregated":false,"geoms":["line"],"coordSystem":"generic","limit":-1},"encodings":{"dimensions":[{"dragId":"gw_X3Vs","fid":"Date","name":"Date","basename":"Date","semanticType":"temporal","analyticType":"dimension"},{"dragId":"gw_IEOC","fid":"GC","name":"GC","basename":"GC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_RSFv","fid":"Operator","name":"Operator","basename":"Operator","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_Wd-n","fid":"DHA Corrected","name":"DHA Corrected","basename":"DHA Corrected","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_7W1u","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"},{"dragId":"gw_mea_key_fid","fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"dragId":"gw_a6t2","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_b_l3","fid":"EPA (mg/g)","name":"EPA (mg/g)","basename":"EPA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_33uP","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_b9Fi","fid":"DHA (mg/g)","name":"DHA (mg/g)","basename":"DHA (mg/g)","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_TCcJ","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"sum"},{"dragId":"gw_count_fid","fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"dragId":"gw_mea_val_fid","fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"dragId":"gw_wv6s","fid":"EPA (%)","name":"EPA (%)","basename":"EPA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"mean"},{"dragId":"gw_4Iv5","fid":"DHA (%)","name":"DHA (%)","basename":"DHA (%)","analyticType":"measure","semanticType":"quantitative","aggName":"mean"},{"dragId":"gw_e2R8","fid":"% Fat","name":"% Fat","basename":"% Fat","analyticType":"measure","semanticType":"quantitative","aggName":"mean"}],"columns":[{"dragId":"gw_CnP9","fid":"Date","name":"Date","basename":"Date","semanticType":"temporal","analyticType":"dimension"}],"color":[{"dragId":"gw_OPRG","fid":"DHA Corrected","name":"DHA Corrected","basename":"DHA Corrected","semanticType":"nominal","analyticType":"dimension"}],"opacity":[{"dragId":"gw_3PfM","fid":"QC","name":"QC","basename":"QC","semanticType":"nominal","analyticType":"dimension"}],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[],"text":[]},"layout":{"showActions":false,"showTableSummary":false,"stack":"stack","interactiveScale":false,"zeroScale":true,"size":{"mode":"fixed","height":476,"width":490},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":false,"opacity":false,"shape":false,"size":false}},"visId":"gw_hcFQ","name":"EPA%, DHA% and Fat% over Time "}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["Operator","GC","QC"],"measures":[{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]},{"workflow":[{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["GC","QC"],"measures":[{"field":"EPA (%)","agg":"mean","asFieldKey":"EPA (%)_mean"},{"field":"EPA (mg/g)","agg":"mean","asFieldKey":"EPA (mg/g)_mean"},{"field":"DHA (%)","agg":"mean","asFieldKey":"DHA (%)_mean"},{"field":"DHA (mg/g)","agg":"mean","asFieldKey":"DHA (mg/g)_mean"},{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]},{"workflow":[{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["QC","GC"],"measures":[{"field":"% Fat","agg":"variance","asFieldKey":"% Fat_variance"},{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]},{"workflow":[{"type":"transform","transform":[{"key":"gw_count_fid","expression":{"op":"one","params":[],"as":"gw_count_fid"}}]},{"type":"view","query":[{"op":"aggregate","groupBy":["Operator"],"measures":[{"field":"EPA (mg/g)","agg":"stdev","asFieldKey":"EPA (mg/g)_stdev"},{"field":"DHA (mg/g)","agg":"stdev","asFieldKey":"DHA (mg/g)_stdev"},{"field":"EPA (%)","agg":"stdev","asFieldKey":"EPA (%)_stdev"},{"field":"DHA (%)","agg":"stdev","asFieldKey":"DHA (%)_stdev"},{"field":"gw_count_fid","agg":"sum","asFieldKey":"gw_count_fid_sum"}]}]}]},{"workflow":[{"type":"view","query":[{"op":"raw","fields":["Date","Operator","GC","% Fat"]}]}]},{"workflow":[{"type":"view","query":[{"op":"raw","fields":["Date","DHA Corrected","QC","EPA (%)","DHA (%)","% Fat"]}]}]}],"timezoneOffsetSeconds":-18000,"version":"0.3.18"}"""

    tableau = pyg.walk(spec, spec=vis_spec, return_html=True, dark='dark')

    return (Conf_Int,
            DHA_Corrected,
            GC,
            Operator,
            QC,
            figs,
            tableau)


