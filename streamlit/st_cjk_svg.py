# bases on https://discuss.streamlit.io/t/display-svg/172

# import textwrap
import streamlit as st

from sklearn.datasets import *
from sklearn import tree
import base64
from io import StringIO

st.write("""# How to use CJK font without installing it and let streamlit support SVG
## Get a CJK font first, for example, 
[NotoSerifCJK-Regular.ttc](https://github.com/googlefonts/noto-cjk/raw/main/Serif/NotoSerifCJK-Regular.ttc)

## Add it to `fontManager` 
""")

with st.echo():
    from matplotlib import pyplot as plt,font_manager as fm
    from pathlib import Path
    import os
    #Restore the `.rcParams` from Matplotlib's internal default style.
    plt.rcdefaults()
    
    path = Path(os.getcwd())
    fname=os.path.join(path.parent.absolute(),'data','NotoSerifCJK-Regular.ttc')
    fontProperties=fm.FontProperties(fname=fname,size=14)
    default_font=fontProperties.get_name()# "Arial Unicode MS"
    if default_font not in [f.name for f in fm.fontManager.ttflist]:
        st.warning(f"{default_font} does not exist, let's add it to fontManager" )

    if fname not in [f.fname for f in fm.fontManager.ttflist]:
        fm.fontManager.addfont(fname) # need absolute path
    
    plt.rcParams['font.sans-serif']=[default_font]+plt.rcParams['font.sans-serif']
    plt.rcParams['axes.unicode_minus']=False # in case minus sign is shown as box

# this one should be after the configuration of matplotlib rcParams
from dtreeviz.trees import *

def decisionTreeViz():
    classifier = tree.DecisionTreeClassifier(max_depth=3)  
    iris = load_iris()
    classifier.fit(iris.data, iris.target)
    #just for test
    feature_names=['萼片sepal length (cm)','sepal width (cm)'
    ,'花瓣petal length (cm)','花瓣petal width (cm)']
    
    class_names=["山鸢尾 (부채붓꽃)", "变色鸢尾(ブルーフラッグ)", "维吉尼亚鸢尾(Iris-virginica)"]
    viz = dtreeviz(classifier,
                iris.data,
                iris.target,
                target_name='variety',
                feature_names=feature_names,
                class_names=class_names  # need class_names for classifier
                )
    return viz


def svg_write(svg, center=True):
    """
    Disable center to left-margin align like other objects.
    """
    # Encode as base 64
    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")

    # Add some CSS on top
    css_justify = "center" if center else "left"
    css = f'<p style="text-align:center; display: flex; justify-content: {css_justify};">'
    html = f'{css}<img src="data:image/svg+xml;base64,{b64}"/>'

    # Write the HTML
    st.write(html, unsafe_allow_html=True)

def seaborn_example():
    import seaborn as sns
    from matplotlib import pyplot as plt

    iris = sns.load_dataset('iris')

    #rename columns to test Chinese 
    iris.columns=['萼片sepal_length', '萼片sepal_width', '花瓣petal_length', '花瓣petal_width',
        'species']
    iris.replace(["setosa","versicolor","virginica"], 
    ["山鸢尾 (부채붓꽃)", "变色鸢尾(ブルーフラッグ)", "维吉尼亚鸢尾(Iris-virginica)"], 
            inplace=True)
    # style used as a theme of graph
    # for example if we want black graph with grid then write "darkgrid"
    sns.set_style("whitegrid",{"font.sans-serif":[default_font]}) 
    #set_style 会 override plt.rcParams['font.serif'],我们再override回来
    # plt.rcParams['font.sans-serif']=[default_font]+plt.rcParams['font.sans-serif']

    fig=sns.pairplot(iris, hue="species")
    return fig

def fig_write(fig, center=True):
    """
    Renders a matplotlib figure object to SVG.
    """
    # Save to stringIO instead of file
    imgdata = StringIO()
    fig.savefig(imgdata, format="svg")

    # Retrieve saved string
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    svg_write(svg_string,center=center)


try:
    st.write("## dtreeviz with CJK support(SVG output)")
    viz=decisionTreeViz()
    svg=viz.svg()
    svg_write(svg)

    st.write("## seaborn with CJK support")
    st.write("### SVG output")
    fig=seaborn_example()
    fig_write(fig)
    st.write("### PNG output")
    st.pyplot(fig)
except Exception as e:
    print(e)
    pass