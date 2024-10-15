import pandas as pd
from scipy.spatial.distance import cdist

##reference: https://stackoverflow.com/questions/38965720/find-closest-point-in-pandas-dataframes
def closest_point(point, points):
    """ Find closest point from a list of points. """
    return points[cdist([point], points).argmin()]

def get_closest_TADs(df1, df2, chr_lst, threshold=7,
                     columns=['Chr', 'Start', 'End', 'DCI_Score']):
    """ Get closest TADs from two dataframes"""
    
    #create empty dataframe to be populated
    df_all = pd.DataFrame(columns=columns+['Coordinate', 'ClosestTAD'])

    for chrom in chr_lst:

        df_ref = df1[df1.Chr==chrom].copy()    
        df_query = df2[df2.Chr==chrom].copy()

        #filter out rows based on DCI threshold
        if threshold == None:
            pass
        elif threshold > 0:
            df_ref = df_ref[df_ref.DCI_Score>=threshold]
            df_ref.reset_index(drop=True, inplace=True)
            df_query = df_query[df_query.DCI_Score>=threshold]
            df_query.reset_index(drop=True, inplace=True)
        elif threshold < 0:
            df_ref = df_ref[df_ref.DCI_Score<=threshold]
            df_ref.reset_index(drop=True, inplace=True)
            df_query = df_query[df_query.DCI_Score<=threshold]
            df_query.reset_index(drop=True, inplace=True)
        else:
            raise Exception('Invalid threshold value. Please provide a positive or \
                            negative integer, or None.')

        if df_query.shape[0] == 0 or df_ref.shape[0] == 0:
            print('Not enough TADs found for chromosome {}'.format(chrom))
            continue

        #print('Chromosome: {}'.format(chrom))
        #print('Number of TADs in query: {}'.format(df_query.shape[0]))
        
        #create TAD coordinates in 2D, to be used for distance calculation
        #note that y is set to 0, as we are only interested in the x-axis
        df_ref['Coordinate'] = [(x, y) for x,y in zip(df_ref['Start'], 
                                                      pd.Series([0]).repeat(df_ref.shape[0]))]
        df_query['Coordinate'] = [(x, y) for x,y in zip(df_query['Start'], 
                                                        pd.Series([0]).repeat(df_query.shape[0]))]
        #find closest TADs between the two dataframes
        df_query['ClosestTAD'] = [closest_point(x, list(df_ref['Coordinate'])) 
                                  for x in df_query['Coordinate']]
        
        #calculate how far these matched TADs are from each other
        coord2 = [tup[0] for tup in df_query['ClosestTAD']]
        df_query['Distance'] = [abs(a - b) for a,b in zip(df_query['Start'], coord2)]
        df_query.sort_values(by='Start', ascending=True, inplace=True)

        #separate rows based on whether ClosestTAD is unique or not
        df_query_nodup = df_query.drop_duplicates(subset='ClosestTAD', keep=False) #no duplicates
        df_query_dup = df_query[df_query.duplicated(subset='ClosestTAD', keep=False)] #all duplicates

        #print('Number of unique TADs: {}'.format(df_query_nodup.shape[0]))
        #print('Number of duplicate TADs: {}'.format(df_query_dup.shape[0]))

        #among duplicates, keep instances with shortest distance
        idx = df_query_dup.groupby(['ClosestTAD'])['Distance'].transform(min) == df_query_dup['Distance']
        df_query_dup = df_query_dup[idx]
        #print('Number of duplicate TADs after filtering: {}'.format(df_query_dup.shape[0]))

        #concatenate dataframes
        df_query = pd.concat([df_query_nodup, df_query_dup])
        df_query.sort_values(by='Start', ascending=True, inplace=True)
        #print('Number of TADs after concatenation: {}'.format(df_query.shape[0]))

        #concat df to df_all
        df_all = pd.concat([df_all, df_query])
        
    df_all.reset_index(drop=True, inplace=True)

    return df_all