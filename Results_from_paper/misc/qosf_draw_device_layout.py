from qiskit_ibm_provider import IBMProvider
import qiskit.visualization as vis

provider = IBMProvider()
backend = provider.get_backend('ibm_osaka')
fig = vis.plot_gate_map(backend,figsize=(12,9),plot_directed=True,font_size=14,line_color=['darkblue']*290)
##fig.suptitle('ibm_kyoto layout')
fig.show()
##fig.savefig('ibm_osaka')

oqc_lucy_coords = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
oqc_lucy_cmap = [[0,1],[1,2],[2,3],[4,3],[4,5],[6,5],[7,6],[0,7]]
fig_oqc = vis.plot_coupling_map(8,oqc_lucy_coords,oqc_lucy_cmap,line_color=['darkblue']*8,plot_directed=True)
fig_oqc.show()
##fig_oqc.savefig('oqc_lucy.png')
