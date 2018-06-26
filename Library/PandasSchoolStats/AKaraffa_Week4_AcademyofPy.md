
# Academy of Py Analysis
**Description:** This script takes in a student information file and a school information file. From there, the script provides 
    data summaries of student head count, school budget and student performance. 

**Key Observations:**
    1. Highest Overall Passing Scores are linked to charter schools with less than 2000 students
    2. Students' reading scores are higher than math scores, regardless of school type or size
    3. Dollars spent per student do not directly correlate with higher overall passing scores
    
**Assumption:** 
    1. Overall Passing Rates are calculated as an average of math and reading; this does not indicate whether students
       are passing BOTH reading and math
    2. Bin sizes have been set to accomodate test data sets and may require adjustment-please review and update if necessary
    3. Passing Threshold has been set at 65, please update the passthreshold variable if necessary
       
       



```python
#Import Dependencies
import pandas as pd
import numpy as np
import os
from collections import OrderedDict
passthreshold=65
```


```python
#Filepath/Read Files/Assign to DataFrame
schoolfilepath="schools_complete.csv"
studentfilepath="students_complete.csv"
school_df=pd.read_csv(schoolfilepath)
student_df=pd.read_csv(studentfilepath)
school_df=school_df.rename(columns={"name":"School"})
student_df=student_df.rename(columns={"school":"School"})
```

### District Summary



```python
#Filter School Table by District
d_schoolfilter=school_df.loc[(school_df["type"] =="District")]
studentschoolinner=pd.merge(school_df,student_df,on="School")
d_students=studentschoolinner.loc[studentschoolinner["type"]=="District",:]
#%Passing Math
d_studentspassmath=d_students.loc[d_students["math_score"]>=passthreshold]
d_studentspassmathcount=d_studentspassmath["Student ID"].nunique()
d_studentspassmathnum=(d_studentspassmathcount/d_students["Student ID"].nunique())*100
#%Passing Reading
d_studentspassreading=d_students.loc[d_students["reading_score"]>=passthreshold]
d_studentspassreadcount=d_studentspassreading["Student ID"].nunique()
d_studentspassreadnum=(d_studentspassreadcount/d_students["Student ID"].nunique())*100
d_studentspassreadnum
#Overall Passing Rate (average of math and reading)
avgpassrate=(d_studentspassreadnum + d_studentspassmathnum)/2
```


```python
#Overall Passing Rate (students passing BOTH math and reading) - This is an additional calculation
pass_readmath=d_students.loc[(d_students["reading_score"]>=passthreshold)&
                                  (d_students["math_score"]>=passthreshold)]
pass_readmathcount=pass_readmath["Student ID"].nunique()
avgpassreadmath=(pass_readmathcount/d_students["Student ID"].nunique())*100
avgpassreadmath
```




    73.52461447212337




```python
#Print District Summary Table
d_summarydata=pd.DataFrame(OrderedDict({
    "Total Schools":[d_schoolfilter["School"].nunique()],"Total Students":[d_students["Student ID"].nunique()],
    "Total Budget":[d_schoolfilter["budget"].sum()],"Average Math Score":[d_students["math_score"].mean()],
     "Average Reading Score":[d_students["reading_score"].mean()],"% Passing Math":[d_studentspassmathnum],
     "% Passing Reading":[d_studentspassreadnum],"Overall Passing Rate":[avgpassrate]
     }))
d_summarydata["Total Students"]=d_summarydata["Total Students"].map("{:,.0f}".format)
d_summarydata["Total Budget"]=d_summarydata["Total Budget"].map("${:,.0f}".format)
d_summarydata["Average Math Score"]=d_summarydata["Average Math Score"].map("{:.2f}".format)
d_summarydata["Average Reading Score"]=d_summarydata["Average Reading Score"].map("{:.2f}".format)
d_summarydata["% Passing Math"]=d_summarydata["% Passing Math"].map("{:.2f}%".format)
d_summarydata["% Passing Reading"]=d_summarydata["% Passing Reading"].map("{:.2f}%".format)
d_summarydata["Overall Passing Rate"]=d_summarydata["Overall Passing Rate"].map("{:.2f}%".format)
d_summarydata
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Total Schools</th>
      <th>Total Students</th>
      <th>Total Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>Overall Passing Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>7</td>
      <td>26,976</td>
      <td>$17,347,923</td>
      <td>76.99</td>
      <td>80.96</td>
      <td>77.82%</td>
      <td>94.48%</td>
      <td>86.15%</td>
    </tr>
  </tbody>
</table>
</div>



*The above chart shows an overall passing rate of 86%, which indicates a student is passing reading or math, but not 
necessary both. The actual rate of passing both reading and math is 74%. 

### School Summary


```python
#GroupBy Schools/Count Students
school_groups=studentschoolinner.groupby("School")
budg_student=school_groups["budget"].max()/school_groups["Student ID"].count()
school_avgread=school_groups["reading_score"].mean()
school_avgmath=school_groups["math_score"].mean()
```


```python
#%Passing Math
st_numpassread=school_groups["reading_score"].apply(lambda x: x[x>=passthreshold].count())
st_perpassread=(st_numpassread/school_groups["Student ID"].count())*100
st_numpassmath=school_groups["math_score"].apply(lambda x: x[x>=passthreshold].count())
st_perpassmath=(st_numpassmath/school_groups["Student ID"].count())*100
st_avgpass=(st_perpassread+st_perpassmath)/2
school_group_df=pd.DataFrame(OrderedDict({"School Type": school_groups["type"].max(),
                                          "Total Students":school_groups["Student ID"].count(),
                              "Total School Budget":school_groups["budget"].max(),
                              "Per Student Budget":budg_student,"Average Math Score":school_avgmath,
                            "Average Reading Score":school_avgread,"% Passing Math":st_perpassmath,
                                "% Passing Reading":st_perpassread,"% Overall Passing":st_avgpass}))
school_group_df_formats=pd.DataFrame(OrderedDict({"School Type": school_groups["type"].max(),
                                          "Total Students":school_groups["Student ID"].count(),
                              "Total School Budget":school_groups["budget"].max(),
                              "Per Student Budget":budg_student,"Average Math Score":school_avgmath,
                            "Average Reading Score":school_avgread,"% Passing Math":st_perpassmath,
                                "% Passing Reading":st_perpassread,"% Overall Passing":st_avgpass}))
school_group_df_formats["Total Students"]=school_group_df_formats["Total Students"].map("{:,.0f}".format)
school_group_df_formats["Total School Budget"]=school_group_df_formats["Total School Budget"].map("${:,.0f}".format)
school_group_df_formats["Per Student Budget"]=school_group_df_formats["Per Student Budget"].map("${:,.2f}".format)
school_group_df_formats["Average Math Score"]=school_group_df_formats["Average Math Score"].map("{:.2f}".format)
school_group_df_formats["Average Reading Score"]=school_group_df_formats["Average Reading Score"].map("{:.2f}".format)
school_group_df_formats["% Passing Math"]=school_group_df_formats["% Passing Math"].map("{:.2f}%".format)
school_group_df_formats["% Passing Reading"]=school_group_df_formats["% Passing Reading"].map("{:.2f}%".format)
school_group_df_formats["%Overall Passing Rate"]=school_group_df_formats["% Overall Passing"].map("{:.2f}%".format)

school_group_df_formats
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing</th>
      <th>%Overall Passing Rate</th>
    </tr>
    <tr>
      <th>School</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>District</td>
      <td>4,976</td>
      <td>$3,124,928</td>
      <td>$628.00</td>
      <td>77.05</td>
      <td>81.03</td>
      <td>77.91%</td>
      <td>94.55%</td>
      <td>86.233923</td>
      <td>86.23%</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1,858</td>
      <td>$1,081,356</td>
      <td>$582.00</td>
      <td>83.06</td>
      <td>83.98</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2,949</td>
      <td>$1,884,411</td>
      <td>$639.00</td>
      <td>76.71</td>
      <td>81.16</td>
      <td>77.18%</td>
      <td>94.54%</td>
      <td>85.859613</td>
      <td>85.86%</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>2,739</td>
      <td>$1,763,916</td>
      <td>$644.00</td>
      <td>77.10</td>
      <td>80.75</td>
      <td>78.20%</td>
      <td>93.87%</td>
      <td>86.035049</td>
      <td>86.04%</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1,468</td>
      <td>$917,500</td>
      <td>$625.00</td>
      <td>83.35</td>
      <td>83.82</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>4,635</td>
      <td>$3,022,020</td>
      <td>$652.00</td>
      <td>77.29</td>
      <td>80.93</td>
      <td>77.73%</td>
      <td>94.61%</td>
      <td>86.170442</td>
      <td>86.17%</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>$248,087</td>
      <td>$581.00</td>
      <td>83.80</td>
      <td>83.81</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2,917</td>
      <td>$1,910,635</td>
      <td>$655.00</td>
      <td>76.63</td>
      <td>81.18</td>
      <td>77.72%</td>
      <td>94.48%</td>
      <td>86.098732</td>
      <td>86.10%</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4,761</td>
      <td>$3,094,650</td>
      <td>$650.00</td>
      <td>77.07</td>
      <td>80.97</td>
      <td>77.97%</td>
      <td>94.48%</td>
      <td>86.221382</td>
      <td>86.22%</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>$585,858</td>
      <td>$609.00</td>
      <td>83.84</td>
      <td>84.04</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>District</td>
      <td>3,999</td>
      <td>$2,547,363</td>
      <td>$637.00</td>
      <td>76.84</td>
      <td>80.74</td>
      <td>77.94%</td>
      <td>94.62%</td>
      <td>86.284071</td>
      <td>86.28%</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1,761</td>
      <td>$1,056,600</td>
      <td>$600.00</td>
      <td>83.36</td>
      <td>83.73</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>Charter</td>
      <td>1,635</td>
      <td>$1,043,130</td>
      <td>$638.00</td>
      <td>83.42</td>
      <td>83.85</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>Charter</td>
      <td>2,283</td>
      <td>$1,319,574</td>
      <td>$578.00</td>
      <td>83.27</td>
      <td>83.99</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>Charter</td>
      <td>1,800</td>
      <td>$1,049,400</td>
      <td>$583.00</td>
      <td>83.68</td>
      <td>83.95</td>
      <td>100.00%</td>
      <td>100.00%</td>
      <td>100.000000</td>
      <td>100.00%</td>
    </tr>
  </tbody>
</table>
</div>



### Display Botton 5 Schools Based on %Total Passing


```python
school_group_df.sort_values("% Overall Passing").head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing</th>
    </tr>
    <tr>
      <th>School</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Figueroa High School</th>
      <td>District</td>
      <td>2949</td>
      <td>1884411</td>
      <td>639.0</td>
      <td>76.711767</td>
      <td>81.158020</td>
      <td>77.178705</td>
      <td>94.540522</td>
      <td>85.859613</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>District</td>
      <td>2739</td>
      <td>1763916</td>
      <td>644.0</td>
      <td>77.102592</td>
      <td>80.746258</td>
      <td>78.203724</td>
      <td>93.866375</td>
      <td>86.035049</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>District</td>
      <td>2917</td>
      <td>1910635</td>
      <td>655.0</td>
      <td>76.629414</td>
      <td>81.182722</td>
      <td>77.716832</td>
      <td>94.480631</td>
      <td>86.098732</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>District</td>
      <td>4635</td>
      <td>3022020</td>
      <td>652.0</td>
      <td>77.289752</td>
      <td>80.934412</td>
      <td>77.734628</td>
      <td>94.606257</td>
      <td>86.170442</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>District</td>
      <td>4761</td>
      <td>3094650</td>
      <td>650.0</td>
      <td>77.072464</td>
      <td>80.966394</td>
      <td>77.966814</td>
      <td>94.475950</td>
      <td>86.221382</td>
    </tr>
  </tbody>
</table>
</div>



### Display Top 5 Schools Based on %Total Passing


```python
school_group_df.sort_values("% Overall Passing",ascending=False).head(5)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>School Type</th>
      <th>Total Students</th>
      <th>Total School Budget</th>
      <th>Per Student Budget</th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing</th>
    </tr>
    <tr>
      <th>School</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Cabrera High School</th>
      <td>Charter</td>
      <td>1858</td>
      <td>1081356</td>
      <td>582.0</td>
      <td>83.061895</td>
      <td>83.975780</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>Charter</td>
      <td>1468</td>
      <td>917500</td>
      <td>625.0</td>
      <td>83.351499</td>
      <td>83.816757</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>Charter</td>
      <td>427</td>
      <td>248087</td>
      <td>581.0</td>
      <td>83.803279</td>
      <td>83.814988</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>Charter</td>
      <td>962</td>
      <td>585858</td>
      <td>609.0</td>
      <td>83.839917</td>
      <td>84.044699</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>Charter</td>
      <td>1761</td>
      <td>1056600</td>
      <td>600.0</td>
      <td>83.359455</td>
      <td>83.725724</td>
      <td>100.0</td>
      <td>100.0</td>
      <td>100.0</td>
    </tr>
  </tbody>
</table>
</div>



### Average Math Score by Grade/School


```python
mathavgbygrade=studentschoolinner["math_score"].groupby([studentschoolinner["School"],studentschoolinner["grade"]]).mean().unstack()
mathavgbygrade
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>grade</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
      <th>9th</th>
    </tr>
    <tr>
      <th>School</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>76.996772</td>
      <td>77.515588</td>
      <td>76.492218</td>
      <td>77.083676</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>83.154506</td>
      <td>82.765560</td>
      <td>83.277487</td>
      <td>83.094697</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>76.539974</td>
      <td>76.884344</td>
      <td>77.151369</td>
      <td>76.403037</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>77.672316</td>
      <td>76.918058</td>
      <td>76.179963</td>
      <td>77.361345</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>84.229064</td>
      <td>83.842105</td>
      <td>83.356164</td>
      <td>82.044010</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>77.337408</td>
      <td>77.136029</td>
      <td>77.186567</td>
      <td>77.438495</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>83.429825</td>
      <td>85.000000</td>
      <td>82.855422</td>
      <td>83.787402</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>75.908735</td>
      <td>76.446602</td>
      <td>77.225641</td>
      <td>77.027251</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>76.691117</td>
      <td>77.491653</td>
      <td>76.863248</td>
      <td>77.187857</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>83.372000</td>
      <td>84.328125</td>
      <td>84.121547</td>
      <td>83.625455</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>76.612500</td>
      <td>76.395626</td>
      <td>77.690748</td>
      <td>76.859966</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>82.917411</td>
      <td>83.383495</td>
      <td>83.778976</td>
      <td>83.420755</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>83.087886</td>
      <td>83.498795</td>
      <td>83.497041</td>
      <td>83.590022</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>83.724422</td>
      <td>83.195326</td>
      <td>83.035794</td>
      <td>83.085578</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>84.010288</td>
      <td>83.836782</td>
      <td>83.644986</td>
      <td>83.264706</td>
    </tr>
  </tbody>
</table>
</div>




```python
readavgbygrade=studentschoolinner["reading_score"].groupby([studentschoolinner["School"],studentschoolinner["grade"]]).mean().unstack()
readavgbygrade

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>grade</th>
      <th>10th</th>
      <th>11th</th>
      <th>12th</th>
      <th>9th</th>
    </tr>
    <tr>
      <th>School</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Bailey High School</th>
      <td>80.907183</td>
      <td>80.945643</td>
      <td>80.912451</td>
      <td>81.303155</td>
    </tr>
    <tr>
      <th>Cabrera High School</th>
      <td>84.253219</td>
      <td>83.788382</td>
      <td>84.287958</td>
      <td>83.676136</td>
    </tr>
    <tr>
      <th>Figueroa High School</th>
      <td>81.408912</td>
      <td>80.640339</td>
      <td>81.384863</td>
      <td>81.198598</td>
    </tr>
    <tr>
      <th>Ford High School</th>
      <td>81.262712</td>
      <td>80.403642</td>
      <td>80.662338</td>
      <td>80.632653</td>
    </tr>
    <tr>
      <th>Griffin High School</th>
      <td>83.706897</td>
      <td>84.288089</td>
      <td>84.013699</td>
      <td>83.369193</td>
    </tr>
    <tr>
      <th>Hernandez High School</th>
      <td>80.660147</td>
      <td>81.396140</td>
      <td>80.857143</td>
      <td>80.866860</td>
    </tr>
    <tr>
      <th>Holden High School</th>
      <td>83.324561</td>
      <td>83.815534</td>
      <td>84.698795</td>
      <td>83.677165</td>
    </tr>
    <tr>
      <th>Huang High School</th>
      <td>81.512386</td>
      <td>81.417476</td>
      <td>80.305983</td>
      <td>81.290284</td>
    </tr>
    <tr>
      <th>Johnson High School</th>
      <td>80.773431</td>
      <td>80.616027</td>
      <td>81.227564</td>
      <td>81.260714</td>
    </tr>
    <tr>
      <th>Pena High School</th>
      <td>83.612000</td>
      <td>84.335938</td>
      <td>84.591160</td>
      <td>83.807273</td>
    </tr>
    <tr>
      <th>Rodriguez High School</th>
      <td>80.629808</td>
      <td>80.864811</td>
      <td>80.376426</td>
      <td>80.993127</td>
    </tr>
    <tr>
      <th>Shelton High School</th>
      <td>83.441964</td>
      <td>84.373786</td>
      <td>82.781671</td>
      <td>84.122642</td>
    </tr>
    <tr>
      <th>Thomas High School</th>
      <td>84.254157</td>
      <td>83.585542</td>
      <td>83.831361</td>
      <td>83.728850</td>
    </tr>
    <tr>
      <th>Wilson High School</th>
      <td>84.021452</td>
      <td>83.764608</td>
      <td>84.317673</td>
      <td>83.939778</td>
    </tr>
    <tr>
      <th>Wright High School</th>
      <td>83.812757</td>
      <td>84.156322</td>
      <td>84.073171</td>
      <td>83.833333</td>
    </tr>
  </tbody>
</table>
</div>




```python
#Budget Bins500,600,700,800
budgbins=[0,580,605,630,655]
budgbinlabels=["<580","580-605","605-630","630-655"]
# school_group_df["Per Student Budget"]
school_group_df["Student Budget Tiers"]=pd.cut(school_group_df["Per Student Budget"],budgbins,labels=budgbinlabels)
budgroup=school_group_df.groupby("Student Budget Tiers").mean()
budgroup[["Average Math Score","Average Reading Score","% Passing Math","% Passing Reading","% Overall Passing"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing</th>
    </tr>
    <tr>
      <th>Student Budget Tiers</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;580</th>
      <td>83.274201</td>
      <td>83.989488</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>580-605</th>
      <td>83.476713</td>
      <td>83.867873</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>605-630</th>
      <td>81.413283</td>
      <td>82.965140</td>
      <td>92.637996</td>
      <td>98.184620</td>
      <td>95.411308</td>
    </tr>
    <tr>
      <th>630-655</th>
      <td>77.866721</td>
      <td>81.368774</td>
      <td>80.963598</td>
      <td>95.227627</td>
      <td>88.095613</td>
    </tr>
  </tbody>
</table>
</div>




```python
schsizebins=[0,1000,2000,5000]
schsizebinlabels=["<1000","1000-2000","2000-5000"]
school_group_df["School Size"]=pd.cut(school_group_df["Total Students"],bins=schsizebins,labels=schsizebinlabels)
# school_group_df["Per Student Budget"]
schsizegroup=school_group_df.groupby("School Size").mean()
schsizegroup[["Average Math Score","Average Reading Score","% Passing Math","% Passing Reading","% Overall Passing"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing</th>
    </tr>
    <tr>
      <th>School Size</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>&lt;1000</th>
      <td>83.821598</td>
      <td>83.929843</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>1000-2000</th>
      <td>83.374684</td>
      <td>83.864438</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.000000</td>
    </tr>
    <tr>
      <th>2000-5000</th>
      <td>77.746417</td>
      <td>81.344493</td>
      <td>80.582397</td>
      <td>95.143406</td>
      <td>87.862902</td>
    </tr>
  </tbody>
</table>
</div>




```python
schoolscoretype=school_group_df.groupby("School Type").mean()
schoolscoretype[["Average Math Score","Average Reading Score","% Passing Math","% Passing Reading","% Overall Passing"]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Average Math Score</th>
      <th>Average Reading Score</th>
      <th>% Passing Math</th>
      <th>% Passing Reading</th>
      <th>% Overall Passing</th>
    </tr>
    <tr>
      <th>School Type</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Charter</th>
      <td>83.473852</td>
      <td>83.896421</td>
      <td>100.000000</td>
      <td>100.000000</td>
      <td>100.00000</td>
    </tr>
    <tr>
      <th>District</th>
      <td>76.956733</td>
      <td>80.966636</td>
      <td>77.808454</td>
      <td>94.449607</td>
      <td>86.12903</td>
    </tr>
  </tbody>
</table>
</div>


