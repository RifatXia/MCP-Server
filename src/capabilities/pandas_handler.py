import pandas as pd

def analyze_csv(file_path: str, column: str, threshold: int):
    """
    analyze csv file and filter rows based on column value
    returns: filtered dataframe as dict
    """
    try:
        # read csv file
        df = pd.read_csv(file_path)
        
        # filter rows where value > threshold
        filtered_df = df[df[column] > threshold]
        
        # convert filtered dataframe to dict for json response
        result = filtered_df.to_dict(orient='records')
        
        return {
            "status": "success",
            "total_rows": len(df),
            "filtered_rows": len(filtered_df),
            "data": result
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"error processing csv: {str(e)}"
        } 