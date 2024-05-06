# Unit test predict ForecasterAutoregMultiSeriesCustom
# ==============================================================================
import re
import pytest
import numpy as np
import pandas as pd
import joblib
from pathlib import Path
from sklearn.exceptions import NotFittedError
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import make_column_transformer
from sklearn.compose import make_column_selector
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from lightgbm import LGBMRegressor

from skforecast.exceptions import IgnoredArgumentWarning
from skforecast.ForecasterAutoregMultiSeriesCustom import ForecasterAutoregMultiSeriesCustom

# Fixtures
from .fixtures_ForecasterAutoregMultiSeriesCustom import series
from .fixtures_ForecasterAutoregMultiSeriesCustom import exog
from .fixtures_ForecasterAutoregMultiSeriesCustom import exog_predict

THIS_DIR = Path(__file__).parent
series_dict = joblib.load(THIS_DIR/'fixture_sample_multi_series.joblib')
exog_dict = joblib.load(THIS_DIR/'fixture_sample_multi_series_exog.joblib')
end_train = "2016-07-31 23:59:00"
series_dict_train = {k: v.loc[:end_train,] for k, v in series_dict.items()}
exog_dict_train = {k: v.loc[:end_train,] for k, v in exog_dict.items()}
series_dict_test = {k: v.loc[end_train:,] for k, v in series_dict.items()}
exog_dict_test = {k: v.loc[end_train:,] for k, v in exog_dict.items()}

series_2 = pd.DataFrame({'1': pd.Series(np.arange(start=0, stop=50)), 
                         '2': pd.Series(np.arange(start=50, stop=100))})

def create_predictors(y): # pragma: no cover
    """
    Create first 5 lags of a time series.
    """
    lags = y[-1:-6:-1]

    return lags


def create_predictors_14_lags(y): # pragma: no cover
    """
    Create first 5 lags of a time series.
    """
    lags = y[-1:-15:-1]

    return lags


def test_predict_NotFittedError_when_fitted_is_False():
    """
    Test NotFittedError is raised when fitted is False.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor      = LinearRegression(),
                     fun_predictors = create_predictors,
                     window_size    = 5
                 )

    err_msg = re.escape(
        ("This Forecaster instance is not fitted yet. Call `fit` with "
         "appropriate arguments before using predict.")
    )
    with pytest.raises(NotFittedError, match = err_msg):
        forecaster.predict(steps=5)


def test_predict_IgnoredArgumentWarning_when_not_available_self_last_window_for_some_levels():
    """
    Test IgnoredArgumentWarning is raised when last_window is not available for 
    levels because it was not stored during fit.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor      = LinearRegression(),
                     fun_predictors = create_predictors,
                     window_size    = 5
                 )
    forecaster.fit(series=series_2, store_last_window=['1'])

    warn_msg = re.escape(
        ("Levels {'2'} are excluded from prediction "
         "since they were not stored in `last_window` attribute "
         "during training. If you don't want to retrain the "
         "Forecaster, provide `last_window` as argument.")
    )
    with pytest.warns(IgnoredArgumentWarning, match = warn_msg):
        predictions = forecaster.predict(steps=5, levels=['1', '2'], last_window=None)

    expected = pd.DataFrame(
                   data    = np.array([50., 51., 52., 53., 54.]),
                   index   = pd.RangeIndex(start=50, stop=55, step=1),
                   columns = ['1']
               )

    pd.testing.assert_frame_equal(predictions, expected)


@pytest.mark.parametrize("store_last_window",
                         [['1'], False],
                         ids=lambda slw: f"store_last_window: {slw}")
def test_predict_ValueError_when_not_available_self_last_window_for_levels(store_last_window):
    """
    Test ValueError is raised when last_window is not available for all 
    levels because it was not stored during fit.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor      = LinearRegression(),
                     fun_predictors = create_predictors,
                     window_size    = 5
                 )
    forecaster.fit(series=series_2, store_last_window=store_last_window)

    err_msg = re.escape(
        ("No series to predict. None of the series are present in "
         "`last_window` attribute. Provide `last_window` as argument "
         "in predict method.")
    )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.predict(steps=5, levels=['2'], last_window=None)


def test_predict_IgnoredArgumentWarning_when_levels_is_list_and_different_last_index_in_self_last_window_DatetimeIndex():
    """
    Test IgnoredArgumentWarning is raised when levels is a list and have 
    different last index in last_window attribute using a DatetimeIndex.
    """
    series_3 = {
        '1': series_2['1'].copy(),
        '2': series_2['2'].iloc[:30].copy(),
    }
    series_3['1'].index = pd.date_range(start='2020-01-01', periods=50)
    series_3['2'].index = pd.date_range(start='2020-01-01', periods=30)
    
    exog_2 = {
        '1': exog['exog_1'].copy(),
        '2': exog['exog_1'].iloc[:30].copy()
    }
    exog_2['1'].index = pd.date_range(start='2020-01-01', periods=50)
    exog_2['2'].index = pd.date_range(start='2020-01-01', periods=30)
    exog_2_pred = {
        '1': exog_predict['exog_1'].copy()
    }
    exog_2_pred['1'].index = pd.date_range(start='2020-02-20', periods=50)

    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor      = LinearRegression(),
                     fun_predictors = create_predictors,
                     window_size    = 5
                 )
    forecaster.fit(series=series_3, exog=exog_2)

    warn_msg = re.escape(
        ("Only series whose last window ends at the same index "
         "can be predicted together. Series that do not reach the "
         "maximum index, '2020-02-19 00:00:00', are excluded "
         "from prediction: {'2'}.")
    )
    with pytest.warns(IgnoredArgumentWarning, match = warn_msg):
        predictions = forecaster.predict(steps=5, levels=['1', '2'], last_window=None,
                                         exog = exog_2_pred,)

    expected = pd.DataFrame(
                   data    = np.array([50., 51., 52., 53., 54.]),
                   index   = pd.date_range(start='2020-02-20', periods=5),
                   columns = ['1']
               )

    pd.testing.assert_frame_equal(predictions, expected)


@pytest.fixture(params=[('1'  , [50., 51., 52., 53., 54.]), 
                        (['2'], [100., 101., 102., 103., 104.]),
                        (['1', '2'], [[50., 100.],
                                      [51., 101.],
                                      [52., 102.],
                                      [53., 103.],
                                      [54., 104.]])
                        ],
                        ids=lambda d: f'levels: {d[0]}, preds: {d[1]}')
def expected_pandas_dataframe(request):
    """
    This is a pytest fixture. It's a function that can be passed to a
    test so that we have a single block of code that can generate testing
    examples.

    We're using `params` in the call to declare that we want multiple versions
    to be generated. This is similar to the parametrize decorator, but it's difference
    because we can re-use `pd.Series` in multiple tests.
    """
    levels = request.param[0]
    levels_names = [levels] if isinstance(levels, str) else levels
        
    expected_df = pd.DataFrame(
                      data    = request.param[1],
                      columns = levels_names,
                      index   = pd.RangeIndex(start=50, stop=55, step=1)
                  )

    return levels, expected_df


def test_predict_output_when_regressor_is_LinearRegression_with_fixture(expected_pandas_dataframe):
    """
    Test predict output when using LinearRegression as regressor with pytest fixture.
    This test is equivalent to the next one.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor      = LinearRegression(),
                     fun_predictors = create_predictors,
                     window_size    = 5
                 )
    forecaster.fit(series=series_2)
    predictions = forecaster.predict(steps=5, levels=expected_pandas_dataframe[0])

    expected = expected_pandas_dataframe[1]

    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_output_when_regressor_is_LinearRegression():
    """
    Test predict output when using LinearRegression as regressor.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
                    regressor      = LinearRegression(),
                    fun_predictors = create_predictors,
                    window_size    = 5,
                )
    forecaster.fit(series=series_2)
    predictions_1 = forecaster.predict(steps=5, levels='1')
    expected_1 = pd.DataFrame(
                     data    = np.array([50., 51., 52., 53., 54.]),
                     index   = pd.RangeIndex(start=50, stop=55, step=1),
                     columns = ['1']
                 )

    predictions_2 = forecaster.predict(steps=5, levels=['2'])
    expected_2 = pd.DataFrame(
                     data    = np.array([100., 101., 102., 103., 104.]),
                     index   = pd.RangeIndex(start=50, stop=55, step=1),
                     columns = ['2']
                 )

    predictions_3 = forecaster.predict(steps=5, levels=None)
    expected_3 = pd.DataFrame(
                     data    = np.array([[50., 100.],
                                         [51., 101.],
                                         [52., 102.],
                                         [53., 103.],
                                         [54., 104.]]),
                     index   = pd.RangeIndex(start=50, stop=55, step=1),
                     columns = ['1', '2']
                 )

    pd.testing.assert_frame_equal(predictions_1, expected_1)
    pd.testing.assert_frame_equal(predictions_2, expected_2)
    pd.testing.assert_frame_equal(predictions_3, expected_3)


def test_predict_output_when_regressor_is_LinearRegression_with_last_window():
    """
    Test predict output when using LinearRegression as regressor and last_window.
    """
    last_window = pd.DataFrame(
                      {'1': [45, 46, 47, 48, 49], 
                       '2': [95, 96, 97, 98, 99], 
                       '3': [1, 2, 3, 4, 5]}, 
                      index = pd.RangeIndex(start=45, stop=50, step=1)
                  )

    forecaster = ForecasterAutoregMultiSeriesCustom(
                    regressor      = LinearRegression(),
                    fun_predictors = create_predictors,
                    window_size    = 5
                )
    forecaster.fit(series=series_2)
    predictions_1 = forecaster.predict(steps=5, levels='1', last_window=last_window)
    expected_1 = pd.DataFrame(
                     data    = np.array([50., 51., 52., 53., 54.]),
                     index   = pd.RangeIndex(start=50, stop=55, step=1),
                     columns = ['1']
                 )

    predictions_2 = forecaster.predict(steps=5, levels=['2'], last_window=last_window)
    expected_2 = pd.DataFrame(
                     data    = np.array([100., 101., 102., 103., 104.]),
                     index   = pd.RangeIndex(start=50, stop=55, step=1),
                     columns = ['2']
                 )

    predictions_3 = forecaster.predict(steps=5, levels=['1', '2'], last_window=last_window)
    expected_3 = pd.DataFrame(
                     data    = np.array([[50., 100.],
                                         [51., 101.],
                                         [52., 102.],
                                         [53., 103.],
                                         [54., 104.]]),
                     index   = pd.RangeIndex(start=50, stop=55, step=1),
                     columns = ['1', '2']
                 )

    pd.testing.assert_frame_equal(predictions_1, expected_1)
    pd.testing.assert_frame_equal(predictions_2, expected_2)
    pd.testing.assert_frame_equal(predictions_3, expected_3)


def test_predict_output_when_regressor_is_LinearRegression_with_transform_series():
    """
    Test predict output when using LinearRegression as regressor and StandardScaler.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor      = LinearRegression(),
                     fun_predictors = create_predictors,
                     window_size    = 5,
                     transformer_series = StandardScaler()
                 )
    forecaster.fit(series=series)
    predictions = forecaster.predict(steps=5, levels='1')

    expected = pd.DataFrame(
                   data    = np.array([0.52791431, 0.44509712, 0.42176045, 0.48087237, 0.48268008]),
                   index   = pd.RangeIndex(start=50, stop=55, step=1),
                   columns = ['1']
               )
    
    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_output_when_regressor_is_LinearRegression_with_transform_series_as_dict():
    """
    Test predict output when using LinearRegression as regressor and transformer_series
    is a dict with 2 different transformers.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor      = LinearRegression(),
                     fun_predictors = create_predictors,
                     window_size    = 5,
                     transformer_series = {'1': StandardScaler(), '2': MinMaxScaler()}
                 )
    forecaster.fit(series=series)
    predictions = forecaster.predict(steps=5, levels=['1'], suppress_warnings=True)

    expected = pd.DataFrame(
                   data    = np.array([0.59619193, 0.46282914, 0.41738496, 0.48522676, 0.47525733]),
                   index   = pd.RangeIndex(start=50, stop=55, step=1),
                   columns = ['1']
               )
    
    pd.testing.assert_frame_equal(predictions, expected)


@pytest.mark.parametrize("transformer_series", 
                         [StandardScaler(),
                          {'1': StandardScaler(), '2': StandardScaler()}], 
                         ids = lambda tr : f'transformer_series type: {type(tr)}')
def test_predict_output_when_regressor_is_LinearRegression_with_transform_series_and_transform_exog(transformer_series):
    """
    Test predict output when using LinearRegression as regressor, StandardScaler
    as transformer_series and transformer_exog as transformer_exog.
    """
    transformer_exog = ColumnTransformer(
                           [('scale', StandardScaler(), ['exog_1']),
                            ('onehot', OneHotEncoder(), ['exog_2'])],
                           remainder = 'passthrough',
                           verbose_feature_names_out = False
                       )
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor          = LinearRegression(),
                     fun_predictors     = create_predictors,
                     window_size        = 5,
                     transformer_series = transformer_series,
                     transformer_exog   = transformer_exog,
                 )
    forecaster.fit(series=series, exog=exog)
    predictions = forecaster.predict(steps=5, levels='1', exog=exog_predict)

    expected = pd.DataFrame(
                   data    = np.array([0.53267333, 0.44478046, 0.52579563, 0.57391142, 0.54633594]),
                   index   = pd.RangeIndex(start=50, stop=55, step=1),
                   columns = ['1']
               )
    
    pd.testing.assert_frame_equal(predictions, expected)


@pytest.mark.parametrize("transformer_series", 
                         [StandardScaler(),
                          {'1': StandardScaler(), '2': StandardScaler()}], 
                         ids = lambda tr : f'transformer_series type: {type(tr)}')
def test_predict_output_when_regressor_is_LinearRegression_with_transform_series_and_transform_exog_different_length_series(transformer_series):
    """
    Test predict output when using LinearRegression as regressor, StandardScaler
    as transformer_series and transformer_exog as transformer_exog with series 
    of different lengths.
    """
    new_series = series.copy()
    new_series['2'].iloc[:10] = np.nan

    transformer_exog = ColumnTransformer(
                           [('scale', StandardScaler(), ['exog_1']),
                            ('onehot', OneHotEncoder(), ['exog_2'])],
                           remainder = 'passthrough',
                           verbose_feature_names_out = False
                       )
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor          = LinearRegression(),
                     fun_predictors     = create_predictors,
                     window_size        = 5,
                     transformer_series = transformer_series,
                     transformer_exog   = transformer_exog,
                 )
    forecaster.fit(series=series, exog=exog)
    predictions = forecaster.predict(steps=5, exog=exog_predict)

    expected = pd.DataFrame(
                   data    = np.array([[0.53267333, 0.55496412],
                                       [0.44478046, 0.57787982],
                                       [0.52579563, 0.66389117],
                                       [0.57391142, 0.65789846],
                                       [0.54633594, 0.5841187 ]]),
                   index   = pd.RangeIndex(start=50, stop=55, step=1),
                   columns = ['1', '2']
               )
    
    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_output_when_categorical_features_native_implementation_HistGradientBoostingRegressor():
    """
    Test predict output when using HistGradientBoostingRegressor and categorical variables.
    """
    df_exog = pd.DataFrame({'exog_1': exog['exog_1'],
                            'exog_2': ['a', 'b', 'c', 'd', 'e']*10,
                            'exog_3': pd.Categorical(['F', 'G', 'H', 'I', 'J']*10)})
    
    exog_predict = df_exog.copy()
    exog_predict.index = pd.RangeIndex(start=50, stop=100)

    categorical_features = df_exog.select_dtypes(exclude=[np.number]).columns.tolist()
    transformer_exog = make_column_transformer(
                           (
                               OrdinalEncoder(
                                   dtype=int,
                                   handle_unknown="use_encoded_value",
                                   unknown_value=-1,
                                   encoded_missing_value=-1
                               ),
                               categorical_features
                           ),
                           remainder="passthrough",
                           verbose_feature_names_out=False,
                       ).set_output(transform="pandas")
    
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor          = HistGradientBoostingRegressor(
                                              categorical_features = categorical_features,
                                              random_state         = 123
                                          ),
                     fun_predictors     = create_predictors,
                     window_size        = 5,
                     transformer_series = None,
                     transformer_exog   = transformer_exog
                 )
    forecaster.fit(series=series, exog=df_exog)
    predictions = forecaster.predict(steps=10, exog=exog_predict)

    expected = pd.DataFrame(
                   data = np.array([[0.55674244, 0.54564144],
                                    [0.39860559, 0.53774558],
                                    [0.53719969, 0.63668042],
                                    [0.7759386 , 0.66871809],
                                    [0.56654221, 0.80858451],
                                    [0.43373393, 0.39998025],
                                    [0.49776999, 0.64896715],
                                    [0.47797067, 0.43578494],
                                    [0.49149785, 0.37087107],
                                    [0.68189581, 0.52863857]]),
                   index   = pd.RangeIndex(start=50, stop=60, step=1),
                   columns = ['1', '2']
               )
    
    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_output_when_categorical_features_native_implementation_LGBMRegressor():
    """
    Test predict output when using LGBMRegressor and categorical variables.
    """
    df_exog = pd.DataFrame({'exog_1': exog['exog_1'],
                            'exog_2': ['a', 'b', 'c', 'd', 'e']*10,
                            'exog_3': pd.Categorical(['F', 'G', 'H', 'I', 'J']*10)})
    
    exog_predict = df_exog.copy()
    exog_predict.index = pd.RangeIndex(start=50, stop=100)

    categorical_features = df_exog.select_dtypes(exclude=[np.number]).columns.tolist()
    transformer_exog = make_column_transformer(
                           (
                               OrdinalEncoder(
                                   dtype=int,
                                   handle_unknown="use_encoded_value",
                                   unknown_value=-1,
                                   encoded_missing_value=-1
                               ),
                               categorical_features
                           ),
                           remainder="passthrough",
                           verbose_feature_names_out=False,
                       ).set_output(transform="pandas")
    
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor          = LGBMRegressor(random_state=123),
                     fun_predictors     = create_predictors,
                     window_size        = 5,
                     transformer_series = None,
                     transformer_exog   = transformer_exog,
                     fit_kwargs         = {'categorical_feature': categorical_features}
                 )
    forecaster.fit(series=series, exog=df_exog)
    predictions = forecaster.predict(steps=10, exog=exog_predict)

    expected = pd.DataFrame(
                   data = np.array([[0.6211422 , 0.73248662],
                                    [0.42283865, 0.45391191],
                                    [0.49351412, 0.661996  ],
                                    [0.71846231, 0.58080355],
                                    [0.55089719, 0.59780378],
                                    [0.39224631, 0.40316854],
                                    [0.46827996, 0.51400857],
                                    [0.67707084, 0.42834292],
                                    [0.45119292, 0.4503941 ],
                                    [0.61998977, 0.65552498]]),
                   index   = pd.RangeIndex(start=50, stop=60, step=1),
                   columns = ['1', '2']
               )
    
    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_output_when_categorical_features_native_implementation_LGBMRegressor_auto():
    """
    Test predict output when using LGBMRegressor and categorical variables with 
    categorical_features='auto'.
    """
    df_exog = pd.DataFrame({'exog_1': exog['exog_1'],
                            'exog_2': ['a', 'b', 'c', 'd', 'e']*10,
                            'exog_3': pd.Categorical(['F', 'G', 'H', 'I', 'J']*10)})
    
    exog_predict = df_exog.copy()
    exog_predict.index = pd.RangeIndex(start=50, stop=100)

    pipeline_categorical = make_pipeline(
                               OrdinalEncoder(
                                   dtype=int,
                                   handle_unknown="use_encoded_value",
                                   unknown_value=-1,
                                   encoded_missing_value=-1
                               ),
                               FunctionTransformer(
                                   func=lambda x: x.astype('category'),
                                   feature_names_out= 'one-to-one'
                               )
                           )
    transformer_exog = make_column_transformer(
                            (
                                pipeline_categorical,
                                make_column_selector(dtype_exclude=np.number)
                            ),
                            remainder="passthrough",
                            verbose_feature_names_out=False,
                       ).set_output(transform="pandas")
    
    forecaster = ForecasterAutoregMultiSeriesCustom(
                     regressor          = LGBMRegressor(random_state=123),
                     fun_predictors     = create_predictors,
                     window_size        = 5,
                     transformer_series = None,
                     transformer_exog   = transformer_exog,
                     fit_kwargs         = {'categorical_feature': 'auto'}
                 )
    forecaster.fit(series=series, exog=df_exog)
    predictions = forecaster.predict(steps=10, exog=exog_predict)

    expected = pd.DataFrame(
                   data = np.array([[0.6211422 , 0.73248662],
                                    [0.42283865, 0.45391191],
                                    [0.49351412, 0.661996  ],
                                    [0.71846231, 0.58080355],
                                    [0.55089719, 0.59780378],
                                    [0.39224631, 0.40316854],
                                    [0.46827996, 0.51400857],
                                    [0.67707084, 0.42834292],
                                    [0.45119292, 0.4503941 ],
                                    [0.61998977, 0.65552498]]),
                   index   = pd.RangeIndex(start=50, stop=60, step=1),
                   columns = ['1', '2']
               )
    
    pd.testing.assert_frame_equal(predictions, expected)


def test_predict_output_when_series_and_exog_dict():
    """
    Test output ForecasterAutoregMultiSeries predict method when series and 
    exog are dictionaries.
    """
    forecaster = ForecasterAutoregMultiSeriesCustom(
        regressor=LGBMRegressor(
            n_estimators=2, random_state=123, verbose=-1, max_depth=2
        ),
        fun_predictors=create_predictors_14_lags,
        window_size=14,
        encoding='ordinal',
        dropna_from_series=False,
        transformer_series=StandardScaler(),
        transformer_exog=StandardScaler(),
    )
    forecaster.fit(
        series=series_dict_train, exog=exog_dict_train, suppress_warnings=True
    )
    predictions = forecaster.predict(
        steps=5, exog=exog_dict_test, suppress_warnings=True
    )
    expected = pd.DataFrame(
        data=np.array(
            [
                [1438.14154717, 2090.79352613, 2166.9832933, 7285.52781428],
                [1438.14154717, 2089.11038884, 2074.55994929, 7488.18398744],
                [1438.14154717, 2089.11038884, 2035.99448247, 7488.18398744],
                [1403.93625654, 2089.11038884, 2035.99448247, 7488.18398744],
                [1403.93625654, 2089.11038884, 2035.99448247, 7488.18398744],
            ]
        ),
        index=pd.date_range(start="2016-08-01", periods=5, freq="D"),
        columns=["id_1000", "id_1001", "id_1003", "id_1004"],
    )

    pd.testing.assert_frame_equal(predictions, expected)