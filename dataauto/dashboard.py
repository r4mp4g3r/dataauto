# dataauto/dashboard.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, classification_report
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import sys

st.title("DataAuto Interactive Dashboard")

uploaded_file = st.file_uploader("Choose a CSV, JSON, or Excel file", type=["csv", "json", "xlsx"])
if uploaded_file is not None:
    file_format = st.radio("Select file format", ["CSV", "JSON", "Excel"])
    try:
        if file_format == "CSV":
            df = pd.read_csv(uploaded_file)
        elif file_format == "JSON":
            df = pd.read_json(uploaded_file)
        elif file_format == "Excel":
            sheet_name = st.text_input("Enter sheet name (leave blank for first sheet):")
            if sheet_name:
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            else:
                df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    st.write("## Data Preview")
    st.dataframe(df.head())

    if st.checkbox("Show Summary Statistics"):
        st.write(df.describe())

    # Visualization Options
    st.write("## Visualizations")
    plot_type = st.selectbox("Select Plot Type", ["Histogram", "Scatter Plot", "Box Plot", "Heatmap", "Line Plot"])

    if plot_type == "Histogram":
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numerical_cols) == 0:
            st.error("No numerical columns available for Histogram.")
        else:
            column = st.selectbox("Select Column for Histogram", numerical_cols)
            fig, ax = plt.subplots()
            sns.histplot(df[column], kde=True, ax=ax)
            plt.title(f'Histogram of {column}')
            st.pyplot(fig)

    elif plot_type == "Scatter Plot":
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numerical_cols) < 2:
            st.error("Need at least two numerical columns for Scatter Plot.")
        else:
            x_col = st.selectbox("Select X-axis Column", numerical_cols)
            y_col = st.selectbox("Select Y-axis Column", numerical_cols)
            fig = px.scatter(df, x=x_col, y=y_col, title=f'Scatter Plot of {x_col} vs {y_col}')
            st.plotly_chart(fig)

    elif plot_type == "Box Plot":
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numerical_cols) == 0:
            st.error("No numerical columns available for Box Plot.")
        else:
            column = st.selectbox("Select Column for Box Plot", numerical_cols)
            fig, ax = plt.subplots()
            sns.boxplot(x=df[column], ax=ax)
            plt.title(f'Box Plot of {column}')
            st.pyplot(fig)

    elif plot_type == "Heatmap":
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numerical_cols) < 2:
            st.error("Not enough numerical columns to generate a heatmap.")
        else:
            selected_cols = st.multiselect("Select Columns for Heatmap", numerical_cols, default=numerical_cols)
            if len(selected_cols) < 2:
                st.error("Please select at least two columns for the heatmap.")
            else:
                corr = df[selected_cols].corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
                plt.title('Heatmap of Numerical Features')
                st.pyplot(fig)

    elif plot_type == "Line Plot":
        numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
        if len(numerical_cols) < 2:
            st.error("Need at least two numerical columns for Line Plot.")
        else:
            x_col = st.selectbox("Select X-axis Column", numerical_cols)
            y_col = st.selectbox("Select Y-axis Column", numerical_cols)
            fig = px.line(df, x=x_col, y=y_col, title=f'Line Plot of {y_col} over {x_col}')
            st.plotly_chart(fig)

    # Machine Learning Integration (Optional)
    st.write("## Machine Learning")
    if st.checkbox("Train a Model"):
        target = st.selectbox("Select Target Column", df.columns)
        available_features = [col for col in df.columns if col != target]
        selected_features = st.multiselect("Select Feature Columns", available_features, default=available_features)

        if not selected_features:
            st.error("Please select at least one feature for training.")
        else:
            model_type = st.selectbox("Select Model Type", ["Regressor", "Classifier"])
            if st.button("Train Model"):
                try:
                    # Separate features and target
                    X = df[selected_features]
                    y = df[target]

                    # Identify categorical and numerical columns
                    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
                    numerical_cols = X.select_dtypes(include=['float64', 'int64']).columns.tolist()

                    if len(numerical_cols) == 0 and len(categorical_cols) == 0:
                        st.error("No feature columns available for training.")
                    else:
                        # Define preprocessing for numerical and categorical data
                        preprocessor = ColumnTransformer(
                            transformers=[
                                ('num', StandardScaler(), numerical_cols),
                                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
                            ])

                        # Select and instantiate the model
                        if model_type == "Regressor":
                            model = Pipeline(steps=[
                                ('preprocessor', preprocessor),
                                ('regressor', RandomForestRegressor(random_state=42))
                            ])
                        else:
                            model = Pipeline(steps=[
                                ('preprocessor', preprocessor),
                                ('classifier', RandomForestClassifier(random_state=42))
                            ])

                        # Split the data
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                        # Fit the model
                        model.fit(X_train, y_train)

                        # Save the model
                        joblib.dump(model, 'trained_model.joblib')

                        # Evaluate the model
                        if model_type == "Regressor":
                            predictions = model.predict(X_test)
                            mse = mean_squared_error(y_test, predictions)
                            r2 = r2_score(y_test, predictions)
                            st.write(f"**Mean Squared Error (MSE):** {mse}")
                            st.write(f"**R² Score:** {r2}")
                        else:
                            predictions = model.predict(X_test)
                            report = classification_report(y_test, predictions)
                            st.text(report)

                        st.success(f"{model_type} trained successfully and saved as `trained_model.joblib`.")

                except Exception as e:
                    st.error(f"Error during model training: {e}")

    # Cleanup (Optional)
    if st.button("Clear Files"):
        try:
            files = os.listdir()
            for file in files:
                if file.endswith('.png') or file.endswith('.html') or file.endswith('.joblib'):
                    os.remove(file)
            st.write("Temporary files cleared.")
        except Exception as e:
            st.error(f"Error clearing files: {e}")