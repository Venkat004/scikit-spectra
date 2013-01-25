''' Plotting wrappers for dataframes, for implementation in pyuvvis.  See plot_utils
for most of the real work.  Recently updated to work on timespectra and not dataframes.'''

__author__ = "Adam Hughes"
__copyright__ = "Copyright 2012, GWU Physics"
__license__ = "Free BSD"
__maintainer__ = "Adam Hughes"
__email__ = "hugadams@gwmail.gwu.edu"
__status__ = "Development"

from plot_utils import _df_colormapper, _uvvis_colors, easy_legend

def _genplot(ts, xlabel, ylabel, title, **pltkwargs):
    ''' Generic wrapper to ts.plot(), that takes in x/y/title as parsed
    from various calling functions.'''
             
    ### Add custom legend interface.  Keyword legstyle does custom ones, if pltkwrd legend==True
    ### For now this could use improvement  
    pltkwargs['legend']=pltkwargs.pop('legend', False)
    legstyle=pltkwargs.pop('legstyle', None)          
            
    ### Make sure don't have "colors", or that 'colors' is not set to default    
    if 'colors' in pltkwargs:
        if pltkwargs['color'].lower()=='default':
            pltkwargs.pop('color')      
    
    if 'colors' in pltkwargs:
        pltkwargs['color']=pltkwargs.pop('colors')    
        print 'Warning: in _genplot, overwriting kwarg "colors" to "color"'
    
    ax=ts.plot(**pltkwargs)
        
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)       
        
    if legstyle and pltkwargs['legend']==True:  #Defaults to false
        if legstyle==0:
            ax.legend(loc='upper center', ncol=8, shadow=True, fancybox=True)  #If l
        if legstyle==1:
            ax.legend(loc='upper left', ncol=2, shadow=True, fancybox=True)  #If l
        if legstyle==2:
            ax=easy_legend(ax, position='top', fancy=True)
    return ax    

	
### The following three plots are simply wrappers to genplot.  Up to the user to pass
### the correct dataframes to fill these plots.
def specplot(ts, **pltkwds):
    ''' Basically a call to gen plot with special attributes, and a default color mapper.'''
    pltkwds['linewidth']=pltkwds.pop('linewidth', 1.0 )    
           
    xlabel=pltkwds.pop('xlabel', ts.full_specunit)  
    ylabel=pltkwds.pop('ylabel', ts.full_iunit+' (Counts)')    
    title=pltkwds.pop('title', str(ts.name) )    
        
    return _genplot(ts, xlabel, ylabel, title, **pltkwds)
    
def timeplot(ts, **pltkwds):
    ''' Sends transposed dataframe into _genplot(); however, this is only useful if one wants to plot
    every single row in a dataframe.  For ranges of rows, see spec_utilities.wavelegnth_slices and
    range_timeplot() below.'''
    pltkwds['color']=pltkwds.pop('color', _df_colormapper(ts, 'jet', axis=1) )         
    pltkwds['legend']=pltkwds.pop('legend', True) #Turn legend on
        
    xlabel=pltkwds.pop('xlabel', ts.full_timeunit)  
    ylabel=pltkwds.pop('ylabel', ts.full_iunit)    
    title=pltkwds.pop('title', str(ts.name) )    
        
    return _genplot(ts.transpose(), xlabel, ylabel, title, **pltkwds)

### Is this worth having? 
def absplot(ts, default='a', **pltkwds):    
    ''' Absorbance plot'''
    ### Make sure ts is absorbance, or readily convertable
    if ts.full_iunit not in ['a', 'a(ln)']:
        ts=ts.as_iunit(default)
                    
    pltkwds['linewidth']=pltkwds.pop('linewidth', 1.0 )   
    
    xlabel=pltkwds.pop('xlabel', ts.full_specunit)  
    ylabel=pltkwds.pop('ylabel', ts.full_timeunit)    
    title=pltkwds.pop('title', 'Absorbance: '+str(ts.name) )    
        
    return _genplot(ts, xlabel, ylabel, title, **pltkwds)

# Requires ranged dataframe used wavelength slices method
def range_timeplot(ranged_ts, **pltkwds):
    ''' Makes plots based on ranged time intervals from spec_utilities.wavelength_slices().
    Uses a special function, _uvvis_colorss() to map the visible spectrum.  Changes default legend
    behavior to true.'''

    pltkwds['color']=pltkwds.pop('color', _uvvis_colors(ranged_ts))
    pltkwds['legend']=pltkwds.pop('legend', True)
    pltkwds['linewidth']=pltkwds.pop('linewidth', 3.0 )  
          
    xlabel=pltkwds.pop('xlabel', ranged_ts.full_timeunit)  
    ylabel=pltkwds.pop('ylabel', ranged_ts.full_iunit)    
    title=pltkwds.pop('title', 'Ranged Time Plot: '+str(ranged_ts.name) )       
                
    return _genplot(ranged_ts.transpose(), xlabel, ylabel, title,**pltkwds)   #ts TRANSPOSE

def areaplot(ranged_ts, **pltkwds):
    ''' Makes plots based on ranged time intervals from spec_utilities.wavelength_slices().
    Uses a special function, _uvvis_colorss() to map the visible spectrum.  Changes default legend
    behavior to true.'''

    pltkwds['legend']=pltkwds.pop('legend', False)
    pltkwds['linewidth']=pltkwds.pop('linewidth', 3.0 )  
          
    xlabel=pltkwds.pop('xlabel', ranged_ts.full_timeunit)  
    ylabel=pltkwds.pop('ylabel', ranged_ts.full_iunit)    
    title=pltkwds.pop('title', 'Area Plot: '+str(ranged_ts.name) )       
                
    return _genplot(ranged_ts.transpose(), xlabel, ylabel, title,**pltkwds)   #ts TRANSPOSE
    

    