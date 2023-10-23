from .. import Unit
import biosteam as bst
from .decorators import cost

__all__ = (
    'WashingTank'
)
# %% Constants

_gal2m3 = 0.003785
_gpm2m3hr = 0.227124
# _m3hr2gpm = 4.40287
_hp2kW = 0.7457
_Gcal2kJ = 4184e3


@cost('Tank volume', 'Tanks', cost=3840e3/8, S=250e3*_gal2m3, 
      CE=522, n=0.7, BM=2.0, N='N_tanks')
@cost('Tank volume', 'Agitators', CE=522, cost=52500,
      S=1e6*_gal2m3, n=0.5, kW=90, BM=1.5, N='N_tanks')
@cost('Flow rate', 'Transfer pumps', kW=58, S=352*_gpm2m3hr,
      cost=47200/5, CE=522, n=0.8, BM=2.3, N='N_tanks')
class WashingTank(Unit):
    """Washing tank system
    **Parameters**   
        **reactions:** [ReactionSet] Washing reactions.
    **ins**    
        [0] Feed        
        [1] Process water        
    **outs**   
        [0] Washed feed

    """
#    purchase_cost = installation_cost = 0
    _N_ins = 2
    _N_outs = 2
    N_tanks = 1
    tau_tank = 5/60/N_tanks #Residence time in each tank
    V_wf = 0.9
    _units = {'Flow rate': 'm3/hr',
              'Tank volume': 'm3'}
    
    def __init__(self, ID='', ins=None, outs=()):
        Unit.__init__(self, ID, ins, outs)

    def _run(self):
        feed, process_solvent = self.ins
        washed,spent_solvent = self.outs
        washed.copy_like(feed)
        spent_solvent.copy_like(process_solvent)   
        # washed.mix_from([feed,process_water])

    def _design(self):
        effluent,spent_solvent = self.outs
        v_0 = effluent.F_vol+spent_solvent.F_vol
        Design = self.design_results
        Design['Tank volume'] = v_0*self.tau_tank/self.V_wf
        Design['Flow rate'] = v_0