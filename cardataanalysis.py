import pandas as pd


def car_analysis():
    car_data = pd.read_csv('autodata_0815.csv')
    print(car_data.head())      # prints first 5 rows
    print(car_data.tail())      # prints last 5 rows
    print(car_data.shape)       # prints out num(rows, col)
                                # since shape is not method != shape()
    print(car_data.iloc[:, :])  # prints all rows/colummns
    print(car_data.loc[:5, 'Price'])    # loc = get row/col with labels
                                        # iloc = get row/col at positions
    print(type(car_data['Mileage']))    # car_data treated like dict
                                        # a column is series object of pandas
    s1 = pd.Series(['Header', 2, 3, 4])
    s2 = pd.Series([1, 2, 'Hello', 'Sup'])

    # creates data frame from defined series
    # pay close attention to formatting .DataFrame([ ])
    frame = pd.DataFrame(
        [
            [1, 2],
            ['Testing', 'Testing']
        ],
        columns=['col1', 'col2'],
        index=['row1', 'row2'])

    frame2 = pd.DataFrame(
        {
            'column1': [1, 2, 3],
            'column2': [2, 4, 6]
        },
        index=['row1', 'row2', 'row3']
    )
    print(frame2)
    print("Mean: " + str(car_data['Price'].mean()))     # pandas.Series.mean method
    print(car_data.mean())
    print(car_data.corr())
    mileage_filter = car_data['Miles/Year'] < 13000
    filtered_mileage = car_data[mileage_filter]
    exterior_filter = (car_data['Miles/Year'] < 13000) & (car_data['Exterior'] == 'Black')
    filtered_exterior = car_data[exterior_filter]
    print(filtered_mileage)
    print(filtered_exterior)


if __name__ == '__main__':
    car_analysis()
