


def prepare_essence (
	essence = {}
):
	this_directory = pathlib.Path (__file__).parent.resolve ()	
	the_mix_directory = str (normpath (join (this_directory, "../..")));

	'''
		"onsite": {
			"host": "0.0.0.0",
			"port": "39000",
			
			"path": crate ("monetary_1/data"),
			"logs_path": crate ("monetary_1/logs/the.logs"),
			"PID_path": crate ("monetary_1/the.process_identity_number"),
		}
	'''
	the_merged_essence = pydash.merge (
		{
			#
			#	summary in vegan.mixes.activate_alert
			#
			"alert_level": "caution",
			
			"CWD": os.getcwd (),
			
			"monetary": {
				"databases": {
					"awesome": {
						"alias": "awesome",
						"collections": [
							"places"
						]
					}
				},

				
				#
				#	_saves
				#		
				#
				"saves": {
					"path":  str (normpath (join (
						the_mix_directory, 
						"adventures/monetary/__saves"
					))),
					
					"exports": {
						"path": str (normpath (join (
							the_mix_directory, 
							"adventures/monetary/__saves/exports"
						)))						
					},
					
					"dumps": {
						"path": str (normpath (join (
							the_mix_directory, 
							"adventures/monetary/__saves/dumps"
						)))
					}					
				}
			},
			
			
			
			"sanique": {
				"directory": str (normpath (join (
					the_mix_directory, 
					"adventures/sanique"
				))),
				
				"path": str (normpath (join (
					the_mix_directory, 
					"adventures/sanique/harbor/on.proc.py"
				))),
				
				
				"harbor": {
					"port": "8000",
					"host": "0.0.0.0"
				},
				
				#
				#	don't modify these currently
				#
				#	These are used for retrieval, but no for launching the
				#	sanic inspector.
				#
				#	https://sanic.dev/en/guide/running/inspector.md#inspector
				#
				"inspector": {
					"port": "7457",
					"host": "0.0.0.0"
				}
			},
			"dictionary": {
				"path": str (normpath (join (the_mix_directory, "__dictionary"))),
				"vegan": str (normpath (join (the_mix_directory, "__dictionary/wedding"))),
			}
		},
		essence
	)

	
	return the_merged_essence