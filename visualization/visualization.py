from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
from pyecharts.charts import PictorialBar, Bar, Pie, Timeline, Radar, Grid, Liquid, Funnel, Page
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.charts import Line
from pyecharts.charts import Sunburst
from pyecharts.charts import Gauge
from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql import functions
import json
from pyecharts.faker import Faker


from pyecharts import options as opts


def read_data():
    spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()
    data = spark.read.format("csv").option("header", "true").load("./datasource/details_final.csv")
    return data

def gender_analyze(data):
    gender_list = []
    #  Gender analysis
    df_gender = data.select(data['CODE_GENDER'])
    gender_num = []
    bin = ['M', 'F']
    # Count the population by groups of gender
    for i in range(2):
        gender_num.append(df_gender.filter(data['CODE_GENDER'] == bin[i]).count())
    gender_list.append(gender_num)
    # Statistics of overdue and paidoff by different groups of gender
    gender_y = []
    for i in range(2):
        y_overdue = df_gender.filter(data['CODE_GENDER'] == bin[i]).filter(data['final_status'] == '0').count()
        y_paidOff = df_gender.filter(data['CODE_GENDER'] == bin[i]).filter(data['final_status'] != '0').count()
        gender_y.append([y_overdue, y_paidOff])
    gender_list.append(gender_y)
    attr = ["Overdue", "PaidOff"]
    pie_male = (
        Pie()
            .add("Male Overall Distribution", [list(z) for z in zip(attr, gender_list[1][0])])
            .set_global_opts(title_opts=opts.TitleOpts(title="Male Overall Distribution"))
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"),
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)")
        )
            .render("male_pie.html")
    )
    pie_female = (
        Pie()
            .add("Female Overall Distribution", [list(z) for z in zip(attr, gender_list[1][1])])
            .set_global_opts(title_opts=opts.TitleOpts(title="Female Overall Distribution"))
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"),
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)")
        )
            .render("female_pie.html")
    )

def age_analyze(data):
    age_bin = [-27375, -21900, -16425, -10950, 0]
    age_list = []
    # Age analysis
    df_age = data.select(data['DAYS_BIRTH'])
    agenum = []
    # Count the population by groups of age
    agenum.append(df_age.filter(data['DAYS_BIRTH'] >= -27375).filter(data['DAYS_BIRTH'] < -21900).count())
    agenum.append(df_age.filter(data['DAYS_BIRTH'] >= -21900).filter(data['DAYS_BIRTH'] < -16425).count())
    agenum.append(df_age.filter(data['DAYS_BIRTH'] >= -16425).filter(data['DAYS_BIRTH'] < -10950).count())
    agenum.append(df_age.filter(data['DAYS_BIRTH'] >= -10950).filter(data['DAYS_BIRTH'] < 0).count())
    age_list.append(agenum)
    # Statistics of overdue and paidoff by different groups of age
    age_y = []

    # Count of overdues
    y_overdue_6075 = df_age.filter(data['DAYS_BIRTH'] >= -27375).filter(data['DAYS_BIRTH'] < -21900). \
        filter(data['final_status'] == '0').count()
    y_overdue_4560 = df_age.filter(data['DAYS_BIRTH'] >= -21900).filter(data['DAYS_BIRTH'] < -16425). \
        filter(data['final_status'] == '0').count()
    y_overdue_3045 = df_age.filter(data['DAYS_BIRTH'] >= -16425).filter(data['DAYS_BIRTH'] < -10950). \
        filter(data['final_status'] == '0').count()
    y_overdue_0030 = df_age.filter(data['DAYS_BIRTH'] >= -10950).filter(data['DAYS_BIRTH'] < 0). \
        filter(data['final_status'] == '0').count()
    age_y.append([y_overdue_6075, y_overdue_4560, y_overdue_3045, y_overdue_0030])

    # Count of paidOffs
    y_paidOff_6075 = df_age.filter(data['DAYS_BIRTH'] >= -27375).filter(data['DAYS_BIRTH'] < -21900). \
        filter(data['final_status'] != '0').count()
    y_paidOff_4560 = df_age.filter(data['DAYS_BIRTH'] >= -21900).filter(data['DAYS_BIRTH'] < -16425). \
        filter(data['final_status'] != '0').count()
    y_paidOff_3045 = df_age.filter(data['DAYS_BIRTH'] >= -16425).filter(data['DAYS_BIRTH'] < -10950). \
        filter(data['final_status'] != '0').count()
    y_paidOff_0030 = df_age.filter(data['DAYS_BIRTH'] >= -10950).filter(data['DAYS_BIRTH'] < 0). \
        filter(data['final_status'] != '0').count()
    age_y.append([y_paidOff_6075, y_paidOff_4560, y_paidOff_3045, y_paidOff_0030])
    age_list.append(age_y)
    attr = ["0-30", "30-45", "45-60", "60-75"]
    bar_age = (
        Bar()
            .add_xaxis(attr)
            .add_yaxis("Overall age distribution", age_list[0])
            .add_yaxis("Overdues", age_list[1][0])
            .add_yaxis("paidOffs", age_list[1][1])
            .set_global_opts(title_opts=opts.TitleOpts(title="Overdue distribution by age group"))
            .render("age_distrbtn.html")
    )

def education_analyze(data):
    educationList = []
    # Education analysis
    df_edu = data.select(data['NAME_EDUCATION_TYPE'])
    edu_num = []
    # Count the population by groups of education level
    edu_num.append(df_edu.filter(data['NAME_EDUCATION_TYPE'] == "Secondary / secondary special").count())
    edu_num.append(df_edu.filter(data['NAME_EDUCATION_TYPE'] == "Higher education").count())
    edu_num.append(df_edu.filter(data['NAME_EDUCATION_TYPE'] != "Higher education"). \
                   filter(data['NAME_EDUCATION_TYPE'] != "Secondary / secondary special").count())
    educationList.append(edu_num)
    # Statistics of overdue and paidoff by different groups of education level
    edu_y = []

    # Count of overdues
    y_overdue_second = df_edu.filter(data['NAME_EDUCATION_TYPE'] == "Secondary / secondary special"). \
        filter(data['final_status'] == '0').count()
    y_overdue_high = df_edu.filter(data['NAME_EDUCATION_TYPE'] == "Higher education"). \
        filter(data['final_status'] == '0').count()
    y_overdue_other = df_edu.filter(data['NAME_EDUCATION_TYPE'] != "Higher education"). \
        filter(data['NAME_EDUCATION_TYPE'] != "Secondary / secondary special"). \
        filter(data['final_status'] == '0').count()
    edu_y.append([y_overdue_second, y_overdue_high, y_overdue_other])

    # Count of paidOffs
    y_paidOff_second = df_edu.filter(data['NAME_EDUCATION_TYPE'] == "Secondary / secondary special"). \
        filter(data['final_status'] != '0').count()
    y_paidOff_high = df_edu.filter(data['NAME_EDUCATION_TYPE'] == "Higher education"). \
        filter(data['final_status'] != '0').count()
    y_paidOff_other = df_edu.filter(data['NAME_EDUCATION_TYPE'] != "Higher education"). \
        filter(data['NAME_EDUCATION_TYPE'] != "Secondary / secondary special"). \
        filter(data['final_status'] != '0').count()
    edu_y.append([y_paidOff_second, y_paidOff_high, y_paidOff_other])

    educationList.append(edu_y)
    edu_level = ["Secondary / secondary special", "Higher education", "other"]
    bar_edu = (
        Bar()
            .add_xaxis(edu_level)
            .add_yaxis("Overall education distribution", educationList[0])
            .add_yaxis("Overdues", educationList[1][0])
            .add_yaxis("paidOffs", educationList[1][1])
            .set_global_opts(title_opts=opts.TitleOpts(title="Overdue distribution by education group"))
            .render("education_distrbtn.html")
    )
    pie_edu_overdue = (
        Pie()
            .add("Female Overall Distribution", [list(z) for z in zip(edu_level, educationList[1][0])])
            .set_global_opts(title_opts=opts.TitleOpts(title="Overdue distribution group by edu_level"))
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"),
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)")
        )
            .set_colors(["green", "blue", "orange"])
            .render("pie_edu_overdue.html")
    )
    pie_edu_paidOff = (
        Pie()
            .add("Female Overall Distribution", [list(z) for z in zip(edu_level, educationList[1][1])])
            .set_global_opts(title_opts=opts.TitleOpts(title="PaidOff distribution group by edu_level"))
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"),
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)")
        )
            .set_colors(["green", "blue", "orange"])
            .render("pie_edu_paidOff.html")
    )

def property_analyze(data):
    possession_list = []
    # Age analysis
    # df_possession = data.select(data['FLAG_OWN_CAR'])
    # df_possession_realty = data.select(data['FLAG_OWN_REALTY'])
    # possession_car_num = []
    # possession_realty_num = []
    possession_num_overdue = []
    possession_num_paidoff = []

    # Count the population by groups of age
    # possession_car_num = df_possession_car.filter(data['FLAG_OWN_CAR'] == 1).count()
    # possession_realty_num = df_possession_realty.filter(data['FLAG_OWN_REALTY'] == 1).count()
    # possession_list.append(possession_car_num + possession_realty_num)

    # Overdue
    # Owns both car and realty
    possession_num_overdue.append(data.filter(data['FLAG_OWN_CAR'] == 1). \
                                  filter(data['FLAG_OWN_REALTY'] == 1). \
                                  filter(data['final_status'] == '0').count())

    # Owns car but no realty
    possession_num_overdue.append(data.filter(data['FLAG_OWN_CAR'] == 1). \
                                  filter(data['FLAG_OWN_REALTY'] == 0). \
                                  filter(data['final_status'] == '0').count())

    # Owns no car but realty
    possession_num_overdue.append(data.filter(data['FLAG_OWN_CAR'] == 0). \
                                  filter(data['FLAG_OWN_REALTY'] == 1). \
                                  filter(data['final_status'] == '0').count())

    # Owns neither car nor realty
    possession_num_overdue.append(data.filter(data['FLAG_OWN_CAR'] == 0). \
                                  filter(data['FLAG_OWN_REALTY'] == 0). \
                                  filter(data['final_status'] == '0').count())

    # possession_num = data.filter(data['final_status'] != '0').count()
    # possession_list.append(possession_num)

    # paidoff
    # Owns both car and realty
    possession_num_paidoff.append(data.filter(data['FLAG_OWN_CAR'] == 1). \
                                  filter(data['FLAG_OWN_REALTY'] == 1). \
                                  filter(data['final_status'] != '0').count())

    # Owns car but no realty
    possession_num_paidoff.append(data.filter(data['FLAG_OWN_CAR'] == 1). \
                                  filter(data['FLAG_OWN_REALTY'] == 0). \
                                  filter(data['final_status'] != '0').count())

    # Owns no car but realty
    possession_num_paidoff.append(data.filter(data['FLAG_OWN_CAR'] == 0). \
                                  filter(data['FLAG_OWN_REALTY'] == 1). \
                                  filter(data['final_status'] != '0').count())

    # Owns neither car nor realty
    possession_num_paidoff.append(data.filter(data['FLAG_OWN_CAR'] == 0). \
                                  filter(data['FLAG_OWN_REALTY'] == 0). \
                                  filter(data['final_status'] != '0').count())

    possession_list.append([possession_num_overdue, possession_num_paidoff])
    c = (
        PictorialBar()
            .add_xaxis(["Own both car and realty", "Own car but no realty",
                        "Own realty but no car", "Own neither"],
                       )
            .add_yaxis(
            "Overdue",
            possession_list[0][0],
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=22,
            symbol_repeat="fixed",
            symbol_offset=[0, 5],
            is_symbol_clip=True,
        )
            .add_yaxis(
            "PaidOff",
            possession_list[0][1],
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=22,
            symbol_repeat="fixed",
            symbol_offset=[0, -30],
            is_symbol_clip=True,
        )
            .reversal_axis()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="Credit status distribution by property owning"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            ),
        )
            .render("property.html")
    )

def house_analyze(data):
    house_list = []
    house_types = ["House / apartment", "With parents", "Municipal apartment", "Rented apartment", "Co-op apartment",
                   "Other"]
    house_apart = []
    house_apart.append(data.filter(data['NAME_HOUSING_TYPE'] == "House / apartment"). \
                       filter(data['final_status'] == '0').count())
    house_apart.append(data.filter(data['NAME_HOUSING_TYPE'] == "House / apartment"). \
                       filter(data['final_status'] != '0').count())
    parents_house = []
    parents_house.append(data.filter(data['NAME_HOUSING_TYPE'] == "With parents"). \
                         filter(data['final_status'] == '0').count())
    parents_house.append(data.filter(data['NAME_HOUSING_TYPE'] == "With parents"). \
                         filter(data['final_status'] != '0').count())
    municipal = []
    municipal.append(data.filter(data['NAME_HOUSING_TYPE'] == "Municipal apartment"). \
                     filter(data['final_status'] == '0').count())
    municipal.append(data.filter(data['NAME_HOUSING_TYPE'] == "Municipal apartment"). \
                     filter(data['final_status'] != '0').count())
    rented = []
    rented.append(data.filter(data['NAME_HOUSING_TYPE'] == "Rented apartment"). \
                  filter(data['final_status'] == '0').count())
    rented.append(data.filter(data['NAME_HOUSING_TYPE'] == "Rented apartment"). \
                  filter(data['final_status'] != '0').count())
    co_op = []
    co_op.append(data.filter(data['NAME_HOUSING_TYPE'] == "Co-op apartment"). \
                 filter(data['final_status'] == '0').count())
    co_op.append(data.filter(data['NAME_HOUSING_TYPE'] == "Co-op apartment"). \
                 filter(data['final_status'] != '0').count())
    other = []
    other.append(data.filter(data['NAME_HOUSING_TYPE'] != "House / apartment"). \
                 filter(data['NAME_HOUSING_TYPE'] != "With parents"). \
                 filter(data['NAME_HOUSING_TYPE'] != "Municipal apartment"). \
                 filter(data['NAME_HOUSING_TYPE'] != "Rented apartment"). \
                 filter(data['NAME_HOUSING_TYPE'] != "Co-op apartment"). \
                 filter(data['final_status'] == '0').count())
    other.append(data.filter(data['NAME_HOUSING_TYPE'] != "House / apartment"). \
                 filter(data['NAME_HOUSING_TYPE'] != "With parents"). \
                 filter(data['NAME_HOUSING_TYPE'] != "Municipal apartment"). \
                 filter(data['NAME_HOUSING_TYPE'] != "Rented apartment"). \
                 filter(data['NAME_HOUSING_TYPE'] != "Co-op apartment"). \
                 filter(data['final_status'] != '0').count())
    house_list.append([house_apart, parents_house, municipal, rented, co_op, other])
    attr_house = ["Overdue", "Paidoff"]
    tl = Timeline()
    for i in range(len(house_types)):
        pie = (
            Pie()
                .add(
                "商家A",
                [list(z) for z in zip(attr_house, house_list[0][i])],
                rosetype="radius",
                radius=["30%", "55%"],
            )
                .set_global_opts(title_opts=opts.TitleOpts("People who live {}".format(house_types[i])))
        )
        tl.add(pie, "{}".format(house_types[i]))
    tl.render("house_types.html")

def children_analyze(data):
    paidoff_y_chil = []
    paidoff_y_chil.append(data.filter(data['CNT_CHILDREN'] == 0). \
                          filter(data['final_status'] != '0').count())
    paidoff_y_chil.append(data.filter(data['CNT_CHILDREN'] == 1). \
                          filter(data['final_status'] != '0').count())
    paidoff_y_chil.append(data.filter(data['CNT_CHILDREN'] == 2). \
                          filter(data['final_status'] != '0').count())
    paidoff_y_chil.append(data.filter(data['CNT_CHILDREN'] == 3). \
                          filter(data['final_status'] != '0').count())
    paidoff_y_chil.append(data.filter(data['CNT_CHILDREN'] == 4). \
                          filter(data['final_status'] != '0').count())
    paidoff_y_chil.append(data.filter(data['CNT_CHILDREN'] == 5). \
                          filter(data['final_status'] != '0').count())
    overdue_y_chil = []

    overdue_y_chil.append(data.filter(data['CNT_CHILDREN'] == 0). \
                          filter(data['final_status'] == '0').count())
    overdue_y_chil.append(data.filter(data['CNT_CHILDREN'] == 1). \
                          filter(data['final_status'] == '0').count())
    overdue_y_chil.append(data.filter(data['CNT_CHILDREN'] == 2). \
                          filter(data['final_status'] == '0').count())
    overdue_y_chil.append(data.filter(data['CNT_CHILDREN'] == 3). \
                          filter(data['final_status'] == '0').count())
    overdue_y_chil.append(data.filter(data['CNT_CHILDREN'] == 4). \
                          filter(data['final_status'] == '0').count())
    overdue_y_chil.append(data.filter(data['CNT_CHILDREN'] == 5). \
                          filter(data['final_status'] == '0').count())
    children_total_list = []

    children_0_total = data.filter(data['CNT_CHILDREN'] == 0).count()
    children_total_list.append(children_0_total)

    children_1_total = data.filter(data['CNT_CHILDREN'] == 1).count()
    children_total_list.append(children_1_total)

    children_2_total = data.filter(data['CNT_CHILDREN'] == 2).count()
    children_total_list.append(children_2_total)

    children_3_total = data.filter(data['CNT_CHILDREN'] == 3).count()
    children_total_list.append(children_3_total)

    children_4_total = data.filter(data['CNT_CHILDREN'] == 4).count()
    children_total_list.append(children_4_total)

    children_5_total = data.filter(data['CNT_CHILDREN'] == 5).count()
    children_total_list.append(children_5_total)
    c = (
        Line()
            .add_xaxis(xaxis_data=["0 child", "1 child", "2 children", "3 children", "4 children", "5 children"])
            .add_yaxis(
            "Overdue",
            y_axis=[round(overdue_y_chil[0] * 100 / children_total_list[0], 2), \
                    round(overdue_y_chil[1] * 100 / children_total_list[1], 2), \
                    round(overdue_y_chil[2] * 100 / children_total_list[2], 2), \
                    round(overdue_y_chil[3] * 100 / children_total_list[3], 2), \
                    round(overdue_y_chil[4] * 100 / children_total_list[4], 2), \
                    round(overdue_y_chil[5] * 100 / children_total_list[5], 2)],
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
            .add_yaxis(
            "Paidoff",
            y_axis=[round(paidoff_y_chil[0] * 100 / children_total_list[0], 2), \
                    round(paidoff_y_chil[1] * 100 / children_total_list[1], 2), \
                    round(paidoff_y_chil[2] * 100 / children_total_list[2], 2), \
                    round(paidoff_y_chil[3] * 100 / children_total_list[3], 2), \
                    round(paidoff_y_chil[4] * 100 / children_total_list[4], 2), \
                    round(paidoff_y_chil[5] * 100 / children_total_list[5], 2)],
            linestyle_opts=opts.LineStyleOpts(width=2),
        )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(name="Number of Children"),
            yaxis_opts=opts.AxisOpts(
                type_="log",
                name="Overdue/Paidoff in percentage %",
                splitline_opts=opts.SplitLineOpts(is_show=True),
                is_scale=True,
                max_=100,
                min_=20,
                interval=10,
            ),
        )
            .render("children_count.html")
    )

def family_analyze(data):
    overdue_y_family = []

    overdue_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Married"). \
                            filter(data['final_status'] == '0').count())
    overdue_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Civil marriage"). \
                            filter(data['final_status'] == '0').count())
    overdue_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Single / not married"). \
                            filter(data['final_status'] == '0').count())
    overdue_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Separated"). \
                            filter(data['final_status'] == '0').count())
    overdue_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Widow"). \
                            filter(data['final_status'] == '0').count())
    paidoff_y_family = []

    paidoff_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Married"). \
                            filter(data['final_status'] != '0').count())
    paidoff_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Civil marriage"). \
                            filter(data['final_status'] != '0').count())
    paidoff_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Single / not married"). \
                            filter(data['final_status'] != '0').count())
    paidoff_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Separated"). \
                            filter(data['final_status'] != '0').count())
    paidoff_y_family.append(data.filter(data['NAME_FAMILY_STATUS'] == "Widow"). \
                            filter(data['final_status'] != '0').count())
    c_schema = [
        {"name": "Married", "max": 25100},
        {"name": "Civil marriage", "max": 3000},
        {"name": "Single / not married", "max": 4900},
        {"name": "Separated", "max": 2200},
        {"name": "Widow", "max": 1600},
    ]
    c = (
        Radar()
            .add_schema(schema=c_schema, shape="circle")
            .add("Paidoff", [paidoff_y_family], linestyle_opts=opts.LineStyleOpts(color="#CD0000"))
            .add("Overdue", [overdue_y_family], linestyle_opts=opts.LineStyleOpts(color="#5CACEE"))
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Credit distribution by family status"))
            .render("family_status.html")
    )
    # family size
    paidoff_family = []

    paidoff_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 1). \
                          filter(data['final_status'] != '0').count())
    paidoff_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 2). \
                          filter(data['final_status'] != '0').count())
    paidoff_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 3). \
                          filter(data['final_status'] != '0').count())
    paidoff_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 4). \
                          filter(data['final_status'] != '0').count())
    paidoff_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 5). \
                          filter(data['final_status'] != '0').count())
    paidoff_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 6). \
                          filter(data['final_status'] != '0').count())
    paidoff_family.append(data.filter(data['CNT_FAM_MEMBERS'] > 6). \
                          filter(data['final_status'] != '0').count())
    overdue_family = []

    overdue_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 1). \
                          filter(data['final_status'] == '0').count())
    overdue_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 2). \
                          filter(data['final_status'] == '0').count())
    overdue_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 3). \
                          filter(data['final_status'] == '0').count())
    overdue_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 4). \
                          filter(data['final_status'] == '0').count())
    overdue_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 5). \
                          filter(data['final_status'] == '0').count())
    overdue_family.append(data.filter(data['CNT_FAM_MEMBERS'] == 6). \
                          filter(data['final_status'] == '0').count())
    overdue_family.append(data.filter(data['CNT_FAM_MEMBERS'] > 6). \
                          filter(data['final_status'] == '0').count())
    family_total = []

    family_1 = data.filter(data['CNT_FAM_MEMBERS'] == 1).count()
    family_total.append(family_1)
    family_2 = data.filter(data['CNT_FAM_MEMBERS'] == 2).count()
    family_total.append(family_2)
    family_3 = data.filter(data['CNT_FAM_MEMBERS'] == 3).count()
    family_total.append(family_3)
    family_4 = data.filter(data['CNT_FAM_MEMBERS'] == 4).count()
    family_total.append(family_4)
    family_5 = data.filter(data['CNT_FAM_MEMBERS'] == 5).count()
    family_total.append(family_5)
    family_6 = data.filter(data['CNT_FAM_MEMBERS'] == 6).count()
    family_total.append(family_6)
    family_6_plus = data.filter(data['CNT_FAM_MEMBERS'] > 6).count()
    family_total.append(family_6_plus)
    x_data = ["Two", "Three", "Four", "Five", "Six", "Seven or more"]
    # y_data = [820, 932, 901, 934, 1290, 1330, 1320]

    (
        Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            "Paidoff",
            y_axis=[40.0, 41.91, 39.79, 38.89, 35.52, 51.72, 64.0],
            linestyle_opts=opts.LineStyleOpts(width=3),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            "Overdue",
            y_axis=[60.0, 58.09, 60.21, 61.11, 64.48, 48.28, 36.0],
            linestyle_opts=opts.LineStyleOpts(width=3),
            label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                name="Overdue/Paidoff in percentage %",

            ),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False, name="family size"),
        )
            .render("family_size.html")
    )

def occupation_analyze(data):
    employed_overdue = data.filter(data['DAYS_EMPLOYED'] <= 0). \
        filter(data['final_status'] == '0').count()
    employed_total = data.filter(data['DAYS_EMPLOYED'] <= 0).count()
    umemployed_overdue = data.filter(data['DAYS_EMPLOYED'] > 0). \
        filter(data['final_status'] == '0').count()
    umemployed_total = data.filter(data['DAYS_EMPLOYED'] > 0).count()
    l1 = (
        Liquid()
            .add("Overdue percentage of the Employed",
                 [0.5938],
                 center=["60%", "50%"],
                 label_opts=opts.LabelOpts(
                     font_size=50,
                     formatter=JsCode(
                         """function (param) {
                                 return (Math.floor(param.value * 10000) / 100) + '%';
                             }"""
                     ),
                     position="inside", ),
                 )
            .set_global_opts(title_opts=opts.TitleOpts(title="Overdue percentage of the people employed"))
            .render("Employed_overdue.html")

    )

    l2 = (
        Liquid()
            .add(
            "Overdue percentage of the Unemployed",
            [0.5786],
            center=["25%", "50%"],
            label_opts=opts.LabelOpts(
                font_size=50,
                formatter=JsCode(
                    """function (param) {
                            return (Math.floor(param.value * 10000) / 100) + '%';
                        }"""
                ),
                position="inside", ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Overdue percentage of the people unemployed"))
            .render("Unemployed_overdue.html")
    )
    working_total = data.filter(data['NAME_INCOME_TYPE'] == "Working").count()
    working_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Working"). \
        filter(data['final_status'] == '0').count()

    working_percent = working_overdue / working_total
    servant_total = data.filter(data['NAME_INCOME_TYPE'] == "State servant").count()
    servant_overdue = data.filter(data['NAME_INCOME_TYPE'] == "State servant"). \
        filter(data['final_status'] == '0').count()

    servant_percent = servant_overdue / servant_total
    commercial_total = data.filter(data['NAME_INCOME_TYPE'] == "Commercial associate").count()
    commercial_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Commercial associate"). \
        filter(data['final_status'] == '0').count()

    commercial_percent = commercial_overdue / commercial_total
    pensioner_total = data.filter(data['NAME_INCOME_TYPE'] == "Pensioner").count()
    pensioner_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Pensioner"). \
        filter(data['final_status'] == '0').count()

    pensioner_percent = pensioner_overdue / pensioner_total
    student_total = data.filter(data['NAME_INCOME_TYPE'] == "Student").count()
    student_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Student"). \
        filter(data['final_status'] == '0').count()
    working_paidoff = data.filter(data['NAME_INCOME_TYPE'] == "Working"). \
        filter(data['final_status'] != '0').count()
    servant_paidoff = data.filter(data['NAME_INCOME_TYPE'] == "State servant"). \
        filter(data['final_status'] != '0').count()
    commercial_paidoff = data.filter(data['NAME_INCOME_TYPE'] == "Commercial associate"). \
        filter(data['final_status'] != '0').count()
    pensioner_paidoff = data.filter(data['NAME_INCOME_TYPE'] == "Pensioner"). \
        filter(data['final_status'] != '0').count()
    student_paidoff = data.filter(data['NAME_INCOME_TYPE'] == "Student"). \
        filter(data['final_status'] != '0').count()
    x_data = ["Working", "State servant", "Commercial associate", "Pensioner", "Student"]
    y_data = [round(working_paidoff * 100 / working_total, 2),
              round(servant_paidoff * 100 / servant_total, 2),
              round(commercial_paidoff * 100 / commercial_total, 2),
              round(pensioner_paidoff * 100 / pensioner_total, 2),
              round(student_paidoff * 100 / student_total, 2)]

    type_data = [[x_data[i], y_data[i]] for i in range(len(x_data))]

    (
        Funnel(init_opts=opts.InitOpts(width="800px", height="500px"))
            .add(
            series_name="",
            data_pair=type_data,
            gap=2,
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
            itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
        )
            .render("imcome_type_paidoff.html")
    )

    # Type
    security_overdue = data.filter(data['OCCUPATION_TYPE'] == "Security staff"). \
        filter(data['final_status'] == '0').count()
    security_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Security staff"). \
        filter(data['final_status'] != '0').count()
    sales_overdue = data.filter(data['OCCUPATION_TYPE'] == "Sales staff"). \
        filter(data['final_status'] == '0').count()
    sales_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Sales staff"). \
        filter(data['final_status'] != '0').count()
    accountants_overdue = data.filter(data['OCCUPATION_TYPE'] == "Accountants"). \
        filter(data['final_status'] == '0').count()
    accountants_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Accountants"). \
        filter(data['final_status'] != '0').count()
    laborers_overdue = data.filter(data['OCCUPATION_TYPE'] == "Laborers"). \
        filter(data['final_status'] == '0').count()
    laborers_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Laborers"). \
        filter(data['final_status'] != '0').count()
    managers_overdue = data.filter(data['OCCUPATION_TYPE'] == "Managers"). \
        filter(data['final_status'] == '0').count()
    managers_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Managers"). \
        filter(data['final_status'] != '0').count()
    drivers_overdue = data.filter(data['OCCUPATION_TYPE'] == "Drivers"). \
        filter(data['final_status'] == '0').count()
    drivers_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Drivers"). \
        filter(data['final_status'] != '0').count()
    core_overdue = data.filter(data['OCCUPATION_TYPE'] == "Core staff"). \
        filter(data['final_status'] == '0').count()
    core_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Core staff"). \
        filter(data['final_status'] != '0').count()
    highTech_overdue = data.filter(data['OCCUPATION_TYPE'] == "High skill tech staff"). \
        filter(data['final_status'] == '0').count()
    highTech_paidoff = data.filter(data['OCCUPATION_TYPE'] == "High skill tech staff"). \
        filter(data['final_status'] != '0').count()
    cleaning_overdue = data.filter(data['OCCUPATION_TYPE'] == "Cleaning staff"). \
        filter(data['final_status'] == '0').count()
    cleaning_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Cleaning staff"). \
        filter(data['final_status'] != '0').count()
    private_overdue = data.filter(data['OCCUPATION_TYPE'] == "Private service staff"). \
        filter(data['final_status'] == '0').count()
    private_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Private service staff"). \
        filter(data['final_status'] != '0').count()
    cooking_overdue = data.filter(data['OCCUPATION_TYPE'] == "Cooking staff"). \
        filter(data['final_status'] == '0').count()
    cooking_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Cooking staff"). \
        filter(data['final_status'] != '0').count()
    lowskill_overdue = data.filter(data['OCCUPATION_TYPE'] == "Low-skill Laborers"). \
        filter(data['final_status'] == '0').count()
    lowskill_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Low-skill Laborers"). \
        filter(data['final_status'] != '0').count()
    medicine_overdue = data.filter(data['OCCUPATION_TYPE'] == "Medicine staff"). \
        filter(data['final_status'] == '0').count()
    medicine_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Medicine staff"). \
        filter(data['final_status'] != '0').count()
    secretaries_overdue = data.filter(data['OCCUPATION_TYPE'] == "Secretaries"). \
        filter(data['final_status'] == '0').count()
    secretaries_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Secretaries"). \
        filter(data['final_status'] != '0').count()
    it_overdue = data.filter(data['OCCUPATION_TYPE'] == "IT staff"). \
        filter(data['final_status'] == '0').count()
    it_paidoff = data.filter(data['OCCUPATION_TYPE'] == "IT staff"). \
        filter(data['final_status'] != '0').count()
    waiter_overdue = data.filter(data['OCCUPATION_TYPE'] == "Waiters/barmen staff"). \
        filter(data['final_status'] == '0').count()
    waiter_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Waiters/barmen staff"). \
        filter(data['final_status'] != '0').count()
    realtyAgent_overdue = data.filter(data['OCCUPATION_TYPE'] == "Realty agents"). \
        filter(data['final_status'] == '0').count()
    realtyAgent_paidoff = data.filter(data['OCCUPATION_TYPE'] == "Realty agents"). \
        filter(data['final_status'] != '0').count()
    hr_overdue = data.filter(data['OCCUPATION_TYPE'] == "HR staff"). \
        filter(data['final_status'] == '0').count()
    hr_paidoff = data.filter(data['OCCUPATION_TYPE'] == "HR staff"). \
        filter(data['final_status'] != '0').count()
    overdue_list = [
        {"value": security_overdue, "percent": security_overdue / (security_overdue + security_paidoff)},
        {"value": sales_overdue, "percent": sales_overdue / (sales_overdue + sales_paidoff)},
        {"value": accountants_overdue, "percent": accountants_overdue / (accountants_overdue + accountants_paidoff)},
        {"value": laborers_overdue, "percent": laborers_overdue / (laborers_overdue + laborers_paidoff)},
        {"value": managers_overdue, "percent": managers_overdue / (managers_overdue + managers_paidoff)},
        {"value": drivers_overdue, "percent": drivers_overdue / (drivers_overdue + drivers_paidoff)},
        {"value": core_overdue, "percent": core_overdue / (core_overdue + core_paidoff)},
        {"value": highTech_overdue, "percent": highTech_overdue / (highTech_overdue + highTech_paidoff)},
        {"value": cleaning_overdue, "percent": cleaning_overdue / (cleaning_overdue + cleaning_paidoff)},
        {"value": private_overdue, "percent": private_overdue / (private_overdue + private_paidoff)},
        {"value": cooking_overdue, "percent": cooking_overdue / (cooking_overdue + cooking_paidoff)},
        {"value": lowskill_overdue, "percent": lowskill_overdue / (lowskill_overdue + lowskill_paidoff)},
        {"value": medicine_overdue, "percent": medicine_overdue / (medicine_overdue + medicine_paidoff)},
        {"value": secretaries_overdue, "percent": secretaries_overdue / (secretaries_overdue + secretaries_paidoff)},
        {"value": it_overdue, "percent": it_overdue / (it_overdue + it_paidoff)},
        {"value": waiter_overdue, "percent": waiter_overdue / (waiter_overdue + waiter_paidoff)},
        {"value": realtyAgent_overdue, "percent": realtyAgent_overdue / (realtyAgent_overdue + realtyAgent_paidoff)},
        {"value": hr_overdue, "percent": hr_overdue / (hr_overdue + hr_paidoff)},
    ]

    paidoff_list = [
        {"value": security_paidoff, "percent": security_paidoff / (security_overdue + security_paidoff)},
        {"value": sales_paidoff, "percent": sales_paidoff / (sales_overdue + sales_paidoff)},
        {"value": accountants_paidoff, "percent": accountants_paidoff / (accountants_overdue + accountants_paidoff)},
        {"value": laborers_paidoff, "percent": laborers_paidoff / (laborers_overdue + laborers_paidoff)},
        {"value": managers_paidoff, "percent": managers_paidoff / (managers_overdue + managers_paidoff)},
        {"value": drivers_paidoff, "percent": drivers_paidoff / (drivers_overdue + drivers_paidoff)},
        {"value": core_paidoff, "percent": core_paidoff / (core_overdue + core_paidoff)},
        {"value": highTech_paidoff, "percent": highTech_paidoff / (highTech_overdue + highTech_paidoff)},
        {"value": cleaning_paidoff, "percent": cleaning_paidoff / (cleaning_overdue + cleaning_paidoff)},
        {"value": private_paidoff, "percent": private_paidoff / (private_overdue + private_paidoff)},
        {"value": cooking_paidoff, "percent": cooking_paidoff / (cooking_overdue + cooking_paidoff)},
        {"value": lowskill_paidoff, "percent": lowskill_paidoff / (lowskill_overdue + lowskill_paidoff)},
        {"value": medicine_paidoff, "percent": medicine_paidoff / (medicine_overdue + medicine_paidoff)},
        {"value": secretaries_paidoff, "percent": secretaries_paidoff / (secretaries_overdue + secretaries_paidoff)},
        {"value": it_paidoff, "percent": it_paidoff / (it_overdue + it_paidoff)},
        {"value": waiter_paidoff, "percent": waiter_paidoff / (waiter_overdue + waiter_paidoff)},
        {"value": realtyAgent_paidoff, "percent": realtyAgent_paidoff / (realtyAgent_overdue + realtyAgent_paidoff)},
        {"value": hr_paidoff, "percent": hr_paidoff / (hr_overdue + hr_paidoff)},
    ]

    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(["Security", "Sale", "Accountants", "Laborer", "Manager", "Driver", "Core staff", \
                        "High Tech", "Cleaning", "Private Service", "Cooking", "Low Tech", \
                        "Medical Service", "Secretary", "IT", "Waiter/Barmen", "Realty Agent", "HR"])
            .add_yaxis("Overdue", overdue_list, stack="stack1", category_gap="50%")
            .add_yaxis("Paidoff", paidoff_list, stack="stack1", category_gap="50%")
            .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                ),
            )
        )
            .render("occupation_type.html")
    )

def income_analyze(data):
    working_total = data.filter(data['NAME_INCOME_TYPE'] == "Working").count()
    working_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Working"). \
        filter(data['final_status'] == '0').count()

    working_percent = working_overdue / working_total
    servant_total = data.filter(data['NAME_INCOME_TYPE'] == "State servant").count()
    servant_overdue = data.filter(data['NAME_INCOME_TYPE'] == "State servant"). \
        filter(data['final_status'] == '0').count()

    servant_percent = servant_overdue / servant_total
    commercial_total = data.filter(data['NAME_INCOME_TYPE'] == "Commercial associate").count()
    commercial_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Commercial associate"). \
        filter(data['final_status'] == '0').count()

    commercial_percent = commercial_overdue / commercial_total
    pensioner_total = data.filter(data['NAME_INCOME_TYPE'] == "Pensioner").count()
    pensioner_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Pensioner"). \
        filter(data['final_status'] == '0').count()

    pensioner_percent = pensioner_overdue / pensioner_total
    student_total = data.filter(data['NAME_INCOME_TYPE'] == "Student").count()
    student_overdue = data.filter(data['NAME_INCOME_TYPE'] == "Student"). \
        filter(data['final_status'] == '0').count()

    student_percent = student_overdue / student_total
    x_data = ["Working", "State servant", "Commercial associate", "Pensioner", "Student"]
    y_data = [59.64, 59.56, 58.73, 57.93, 27.27]

    data = [[x_data[i], y_data[i]] for i in range(len(x_data))]

    (
        Funnel(init_opts=opts.InitOpts(width="800px", height="500px"))
            .add(
            series_name="",
            data_pair=data,
            gap=2,
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
            label_opts=opts.LabelOpts(is_show=True, position="inside"),
            itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="Overdue Percentage Ranking by Different Incoming Types"))
            .render("imcome_type.html")
    )



def annual_analyze(data):
    min_annual = data.filter(data['AMT_INCOME_TOTAL'] < 122000).count()

    min_annual_overdue = data.filter(data['AMT_INCOME_TOTAL'] < 122000). \
        filter(data['final_status'] == '0').count()
    min_annual_paidoff = data.filter(data['AMT_INCOME_TOTAL'] < 122000). \
        filter(data['final_status'] != '0').count()
    annual_50 = data.filter(data['AMT_INCOME_TOTAL'] >= 122000).filter(data['AMT_INCOME_TOTAL'] < 161000).count()

    annual_50_overdue = data.filter(data['AMT_INCOME_TOTAL'] >= 122000).filter(data['AMT_INCOME_TOTAL'] < 161000). \
        filter(data['final_status'] == '0').count()
    annual_50_paidoff = data.filter(data['AMT_INCOME_TOTAL'] >= 122000).filter(data['AMT_INCOME_TOTAL'] < 161000). \
        filter(data['final_status'] != '0').count()
    annual_75 = data.filter(data['AMT_INCOME_TOTAL'] >= 161000).filter(data['AMT_INCOME_TOTAL'] < 225000).count()

    annual_75_overdue = data.filter(data['AMT_INCOME_TOTAL'] >= 161000).filter(data['AMT_INCOME_TOTAL'] < 225000). \
        filter(data['final_status'] == '0').count()
    annual_75_paidoff = data.filter(data['AMT_INCOME_TOTAL'] >= 161000).filter(data['AMT_INCOME_TOTAL'] < 225000). \
        filter(data['final_status'] != '0').count()
    max_annual = data.filter(data['AMT_INCOME_TOTAL'] >= 225000).count()

    max_annual_overdue = data.filter(data['AMT_INCOME_TOTAL'] >= 225000). \
        filter(data['final_status'] == '0').count()
    max_annual_paidoff = data.filter(data['AMT_INCOME_TOTAL'] >= 225000). \
        filter(data['final_status'] != '0').count()

    data = [
        opts.SunburstItem(
            name="Below 122K",
            children=[
                opts.SunburstItem(
                    name="paidoff",
                    value=min_annual_paidoff,
                ),
                opts.SunburstItem(
                    name="overdue",
                    value=min_annual_overdue,
                ),
            ],
        ),
        opts.SunburstItem(
            name="122K - 161K",
            children=[
                opts.SunburstItem(
                    name="paidoff",
                    value=annual_50_paidoff,
                ),
                opts.SunburstItem(
                    name="overdue",
                    value=annual_50_overdue,
                ),
            ],
        ),
        opts.SunburstItem(
            name="161K - 225K",
            children=[
                opts.SunburstItem(
                    name="paidoff",
                    value=annual_75_paidoff,
                ),
                opts.SunburstItem(
                    name="overdue",
                    value=annual_75_overdue,
                ),
            ],
        ),
        opts.SunburstItem(
            name="Above 225K",
            children=[
                opts.SunburstItem(
                    name="paidoff",
                    value=max_annual_paidoff,
                ),
                opts.SunburstItem(
                    name="overdue",
                    value=max_annual_overdue,
                ),
            ],
        ),
    ]

    sunburst = (
        Sunburst(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add(series_name="", data_pair=data, radius=[0, "90%"])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}"))
            .render("annual_income.html")
    )

def employment_analyze(data):
    employed_overdue_total = []
    employed_paidoff_total = []
    employed_min = data.filter(data['DAYS_EMPLOYED'] < -3103).count()

    employed_min_overdue = data.filter(data['DAYS_EMPLOYED'] < -3103). \
        filter(data['final_status'] == '0').count()
    employed_overdue_total.append(employed_min_overdue)

    employed_min_paidoff = data.filter(data['DAYS_EMPLOYED'] < -3103). \
        filter(data['final_status'] != '0').count()
    employed_paidoff_total.append(employed_min_paidoff)
    employed_25 = data.filter(data['DAYS_EMPLOYED'] >= -3103).filter(data['DAYS_EMPLOYED'] < -1467).count()

    employed_25_overdue = data.filter(data['DAYS_EMPLOYED'] >= -3103).filter(data['DAYS_EMPLOYED'] < -1467). \
        filter(data['final_status'] == '0').count()
    employed_overdue_total.append(employed_25_overdue)

    employed_25_paidoff = data.filter(data['DAYS_EMPLOYED'] >= -3103).filter(data['DAYS_EMPLOYED'] < -1467). \
        filter(data['final_status'] != '0').count()
    employed_paidoff_total.append(employed_25_paidoff)
    employed_50 = data.filter(data['DAYS_EMPLOYED'] >= -1467).filter(data['DAYS_EMPLOYED'] < -371).count()

    employed_50_overdue = data.filter(data['DAYS_EMPLOYED'] >= -1467).filter(data['DAYS_EMPLOYED'] < -371). \
        filter(data['final_status'] == '0').count()
    employed_overdue_total.append(employed_50_overdue)

    employed_50_paidoff = data.filter(data['DAYS_EMPLOYED'] >= -1467).filter(data['DAYS_EMPLOYED'] < -371). \
        filter(data['final_status'] != '0').count()
    employed_paidoff_total.append(employed_50_paidoff)
    employed_max = data.filter(data['DAYS_EMPLOYED'] >= -371).filter(data['DAYS_EMPLOYED'] < 0).count()

    employed_max_overdue = data.filter(data['DAYS_EMPLOYED'] >= -371).filter(data['DAYS_EMPLOYED'] < 0). \
        filter(data['final_status'] == '0').count()
    employed_overdue_total.append(employed_max_overdue)

    employed_max_paidoff = data.filter(data['DAYS_EMPLOYED'] >= -371).filter(data['DAYS_EMPLOYED'] < 0). \
        filter(data['final_status'] != '0').count()
    employed_paidoff_total.append(employed_max_paidoff)
    c = (
        Bar()
            .add_xaxis(["Above 8 years", "2 - 8 years", "1 - 2 years", "Below 1 year"])
            .add_yaxis("Overdue", employed_overdue_total)
            .add_yaxis("Paidoff", employed_paidoff_total)
            .reversal_axis()
            .set_series_opts(label_opts=opts.LabelOpts(position="right"))
            .set_global_opts(
            yaxis_opts=opts.AxisOpts(name="Employed Days", ),
            xaxis_opts=opts.AxisOpts(name="Population of Overdue/Paidoff"),
        )
            .render("employed_days.html")
    )

def contact_analyze(data):
    full_contact_overdue = data.filter(data['FLAG_MOBIL'] == 1).filter(data['FLAG_WORK_PHONE'] == 1). \
        filter(data['FLAG_PHONE'] == 1).filter(data['FLAG_EMAIL'] == 1). \
        filter(data['final_status'] == '0').count()

    full_contact = data.filter(data['FLAG_MOBIL'] == 1).filter(data['FLAG_WORK_PHONE'] == 1). \
        filter(data['FLAG_PHONE'] == 1).filter(data['FLAG_EMAIL'] == 1).count()

    full_contact_percent = full_contact_overdue / full_contact
    nonfull_contact_overdue = data.filter(data['final_status'] == 0).count() - full_contact_overdue

    nonfull_contact = 36457 - full_contact

    nonfull_contact_percent = nonfull_contact_overdue / nonfull_contact


    c = (
        Gauge()
            .add("Overdue Percentage", [("", round(full_contact_percent * 100))])
            .render("full_contact_overdue.html")
    )
    c = (
        Gauge()
            .add("Overdue Percentage", [("", round(nonfull_contact_percent * 100))])
            .render("nonfull_contact_overdue.html")
    )

if __name__ == '__main__':
    data = read_data()
    gender_analyze(data)
    age_analyze(data)
    education_analyze(data)
    property_analyze(data)
    house_analyze(data)
    children_analyze(data)
    family_analyze(data)
    occupation_analyze(data)
    income_analyze(data)
    annual_analyze(data)
    employment_analyze(data)
    contact_analyze(data)
