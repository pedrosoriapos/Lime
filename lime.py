import lime
import lime.lime_tabular

num_features = 20
rf_fn = lambda x: rf.predict(x).astype(float)

explainer = lime.lime_tabular.LimeTabularExplainer(training_data = np.array(X),
                                                   training_labels = X.columns,
                                                   feature_names = X.columns,
                                                   class_names = ['Class 0', 'Class 1'],
                                                   categorical_features = list(np.array(np.where((X.nunique() <= 2).values))[0]))

lime = X.apply(lambda x: explainer.explain_instance(data_row = x, predict_fn = rf_fn, num_features = num_features).as_list(), axis = 1)

lime_vars = lime_sbe.apply(lambda x: [i[0] for i in x])
lime_values = lime_sbe.apply(lambda x: [i[1] for i in x])
X_lime = df
for i in np.arange(1, 21, 1):
    X_lime['var_{}'.format(i)] = lime_vars.apply(lambda x: x[i - 1])
    X_lime['coef_var_{}'.format(i)] = lime_values.apply(lambda x: x[i - 1])
X_lime['score'] = rf.predict_proba(X)[:,1]

df_var = df[['var_{}'.format(i) for i in np.arange(1, num_features + 1, 1)]]
df_coef = df[['coef_var_{}'.format(i) for i in np.arange(1, num_features + 1, 1)]]

df_var_melt = pd.melt(df_var, id_vars = [index], value_vars = ['var_{}'.format(i) for i in np.arange(1, num_features + 1, 1)])
df_affl_var_melt = df_var_melt.sort_values(by = [index])
df_coef_melt = pd.melt(df_coef, id_vars = [index], value_vars = ['coef_var_{}'.format(i) for i in np.arange(1, num_features + 1, 1)])
df_coef_melt = df_coef_melt.sort_values(by = [index])

df_coef_melt.variable = df_coef_melt.variable.apply(lambda x: x[5:])
df_melt = df_var_melt.merge(df_coef_melt, on = index + ['variable'], how = 'left').drop('variable', axis = 1)
