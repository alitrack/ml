# bases on https://discuss.streamlit.io/t/display-svg/172

import streamlit as st
from sklearn.datasets import *
from sklearn.tree import DecisionTreeClassifier
from dtreeviz.trees import dtreeviz
import base64

def decisionTreeViz():
    classifier = DecisionTreeClassifier(max_depth=3)  
    iris = load_iris()
    classifier.fit(iris.data, iris.target)

    viz = dtreeviz(classifier,
                iris.data,
                iris.target,
                target_name='variety',
                feature_names=iris.feature_names,
                class_names=["setosa","versicolor","virginica"]  # need class_names for classifier
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

viz=decisionTreeViz()
svg=viz.svg()
svg_write(svg)