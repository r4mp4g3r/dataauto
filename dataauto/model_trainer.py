# dataauto/model_trainer.py

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, classification_report
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import sys

def preprocess_features(X):
    """
    Preprocess features by handling numerical and categorical variables.

    Parameters:
        X (pd.DataFrame): Features.

    Returns:
        ColumnTransformer: Preprocessing pipeline.
    """
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    return preprocessor

def train_model(df, target, model_type='regressor', test_size=0.2, random_state=42):
    """
    Train a machine learning model and return the model and evaluation report.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        target (str): Target column name.
        model_type (str): Type of model to train ('regressor' or 'classifier').
        test_size (float): Proportion of data to include in the test set.
        random_state (int): Random state for reproducibility.

    Returns:
        Pipeline: Trained model pipeline.
        str: Evaluation report.
    """
    try:
        if target not in df.columns:
            raise ValueError(f"Target column '{target}' does not exist in the dataset.")

        # Features and target
        X = df.drop(columns=[target])
        y = df[target]

        # Preprocess features
        preprocessor = preprocess_features(X)

        # Select and instantiate the model
        if model_type.lower() == "regressor":
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('regressor', RandomForestRegressor(random_state=random_state))
            ])
        elif model_type.lower() == "classifier":
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', RandomForestClassifier(random_state=random_state))
            ])
        else:
            raise ValueError("Unsupported model type. Choose 'regressor' or 'classifier'.")

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

        # Fit the model
        model.fit(X_train, y_train)

        # Evaluate the model
        if model_type.lower() == "regressor":
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)
            report = f"Mean Squared Error (MSE): {mse}\nR^2 Score: {r2}\n"
        else:
            predictions = model.predict(X_test)
            report = classification_report(y_test, predictions, zero_division=0)

        return model, report

    except Exception as e:
        print(f"Error during model training: {e}")
        sys.exit(1)