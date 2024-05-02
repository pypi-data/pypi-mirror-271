from pathlib import Path
from pickle import dump
import os

import pandas as pd 
import matplotlib.pyplot as plt
import torch
from torcheval.metrics.functional import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import  StandardScaler, MinMaxScaler


def import_lpc_data(path, delimiter=','):
    '''
    Imports data into a pandas dataFrame from csv
    -------
    Input:
    ------
    path: path
        path where the data is stored
    delimiter: str
        delimiter between columns of csv
    Output:
    -------
    data: pandas dataframe 
        dataframe with data
    '''
    data = pd.read_csv(path, delimiter=delimiter)
    return data

def data_to_input_output_tensors(data, input_param=None, output_param=None, verbosity=False):
    '''Preprocessing function that creates the input and output tensors
    ---------
    Input:
    -----
    data: pd.Dataframe
        hLPC optimization data
    input_param: list
        list of input parameters used to tain de neural network, ['C1_up2_thick','C1_up2_dop','C1_down1_thick','C1_down1_dop','wavelength'] by default
    output_param: list
        list of output parameter(s) used to tain de neural network, ['Eff'] by default
    verbosity: bool
        Print information about the final scaled tensors
    Output:
    ------
    X_list: torch.tensor
        Input tensor
    Y_list: torch.tensor
        Output tensor
    '''
    if not input_param:
        print('List of input parameters to feed the neural network not defined')
    if not output_param:
        print('List of output parameter(s) to feed the neural network not defined')
    df_inputs = pd.DataFrame(data, columns=input_param)
    df_outputs = pd.DataFrame(data, columns=output_param)
    X_list, Y_list = df_inputs.to_numpy(), df_outputs.to_numpy()
    if verbosity:
        print("Total size\n","\tInput:", torch.tensor(X_list, dtype=torch.float32).shape,"\tOutput:",torch.tensor(Y_list, dtype=torch.float32).shape)
    return torch.tensor(X_list, dtype=torch.float32), torch.tensor(Y_list, dtype=torch.float32)


def split_data(X, Y, test_split = 0.2, verbosity=False):
    '''Split data into train, validation and test subsets
    ---------
    Input:
    ------
    X: torch.tensor
        Input tensor
    Y: torch.tensor
        Output tensor
    test_split: float
        Percentage of subsets distribution, 20% test by default
    
    Output:
    -------
    X_train, Y_train: torch.tensor
        Input, Output train subsets
    X_val, Y_val: torch.tensor
        Input, Output validation subsets
    X_test, Y_test: torch.tensor
        Input, Output test subsets
    '''
    X, X_test, Y, Y_test = train_test_split(X, Y, test_size=test_split) 
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=test_split)
    if verbosity:
        print("Train size\n","\tInput:", X_train.shape,"\tOutput:",Y_train.shape)
        print("Validation size\n","\tInput:", X_val.shape,"\tOutput:",Y_val.shape)
        print("Test size\n","\tInput:", X_test.shape,"\tOutput:",Y_test.shape)
    return X_train, X_val, X_test, Y_train, Y_val, Y_test


def scale_input(X_train, X_val, X_test, scaler='standard'):
    '''Preprocessing function that normalize the input and output of the neural network and store the scalers
    ---------
    Input:
    -----
    data: pd.Dataframe
        hLPC optimization data
    scaler: str
        Choose the scaler to apply to the data, two options: StandardScaler 'standard' (default) and MinMaxScaler 'minmax'

    Output:
    ------
    X_train: torch.tensor
        Input train tensor
    X_val: torch.tensor
        Input validation tensor
    X_test: torch.tensor
        Input test tensor
    scaler_inputs: object
        Scaler object for inputs, standard by default
    '''
    if scaler == 'standard':
        scaler_inputs = StandardScaler()
    elif scaler == 'minmax':
        scaler_inputs = MinMaxScaler()
    X_train_scaled = scaler_inputs.fit_transform(X_train)
    X_val_scaled = scaler_inputs.transform(X_val)
    X_test_scaled = scaler_inputs.transform(X_test)
    directory =  'scaler_objects/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    dump(scaler_inputs, open(directory+'scaler_inputs.pkl', 'wb'))
    return torch.tensor(X_train_scaled, dtype=torch.float32), torch.tensor(X_val_scaled, dtype=torch.float32), torch.tensor(X_test_scaled, dtype=torch.float32), scale_input


def scale_output(Y_train, Y_val, Y_test, scaler='standard'):
    '''Preprocessing function that normalize the input and output of the neural network and store the scalers
    ---------
    Input:
    -----
    data: pd.Dataframe
        hLPC optimization data
    scaler: str
        Choose the scaler to apply to the data, two options: StandardScaler 'standard' (default) and MinMaxScaler 'minmax'
    Output:
    ------
    Y_train: torch.tensor
        Output tensor
    Y_val: torch.tensor
        Output tensor
    Y_test: torch.tensor
        Output tensor
    scaler_outputs: object
        Scaler object for outputs, standard by default
    '''
    if scaler == 'standard':
        scaler_output = StandardScaler()
    elif scaler == 'minmax':
        scaler_output = MinMaxScaler()
    Y_train_scaled = scaler_output.fit_transform(Y_train)
    Y_val_scaled = scaler_output.transform(Y_val)
    Y_test_scaled = scaler_output.transform(Y_test)
    directory =  'scaler_objects/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    dump(scale_output, open(directory+'scaler_output.pkl', 'wb'))
    return torch.tensor(Y_train_scaled, dtype=torch.float32), torch.tensor(Y_val_scaled, dtype=torch.float32), torch.tensor(Y_test_scaled, dtype=torch.float32), scaler_output


def prediction_versus_simulation_plot(simulation, prediction, r2, xlabel = None, ylabel = None, rms = None, storepath = None):
    '''Plot for the comparison of the simulated versus predicted data with machine learning
    --------------------
    Parameters:
    ------
    simulation: list or torch.tensor
        Simulated data
    prediction: list or torch.tensor
        Predicted data
    r2: float
        Coefficient of determination between simulated and predicted data
    xlabel: str
        Text for the xlabel
    ylabel: str
        Text fot the ylabel
    rms: list 
        Root mean square errors in the prediction of each value
    storepath: str
        Path to store the plot, by default is stored in the execution directory
    '''
    fig, ax = plt.subplots()
    if rms:
        rms = mean_squared_error(simulation, prediction)**0.5
        plt.errorbar(simulation, prediction, fmt='.', yerr=rms, label='RMSE')
    else:
        plt.plot(simulation, prediction,'.',color='darkorange',markersize=15,alpha=0.8)
    plt.xlabel(xlabel,fontsize=20)
    plt.ylabel(ylabel,fontsize=20)
    plt.plot(simulation, simulation,'-', color='darkgrey')
    textstr0 = rf'$R^2$={r2}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.3)
    plt.text(x=0.1,y=0.8, s=textstr0, transform=ax.transAxes, fontsize=20,
        verticalalignment='top', bbox=props)
    plt.locator_params(axis='x', nbins=6)
    plt.locator_params(axis='y', nbins=6)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    if storepath:
        plt.savefig(Path(storepath,f'prediction_vs_simulation.pdf'), bbox_inches='tight')
    else:
        plt.savefig('prediction_vs_simulation.pdf', bbox_inches='tight')
    plt.show()
    plt.close()
