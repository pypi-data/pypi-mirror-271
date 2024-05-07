
from skysurvey.target.snia import SNeIaMagnitude
from . import agepop, magnitude, lss


__all__ = ["brokenalpha_model"]

agestep_model = {"prompt": {"func": agepop.get_promptpdf,
                        "kwargs":{"redshift":"@z", "k":0.75}
                       },
                "magabs": {"func": SNeIaMagnitude.tripp_and_step,
                           "kwargs": {"x1":"@x1", "c":"@c", "isup":"@prompt"}
                           }
                }
                               

brokenalpha_model = {"prompt": {"func": agepop.get_promptpdf,
                        "kwargs":{"redshift":"@z", "k":0.75}
                       },
                
                    "mass":{"func": agepop.get_hostmass_pdf,
                            "kwargs":{"fprompt":"@prompt", "redshift":"@z"}
                          },
                          
                    "localcolor": {"func": agepop.hostmass_to_color, 
                            "kwargs":{"fprompt":"@prompt", "mass":"@mass"}
                           },
                           
                    "x1mode": {"func": agepop.get_stretchmode, 
                        "kwargs":{"fprompt":"@prompt", "ratio_old":0.4}
                        },
             
                    "x1": {"func": agepop.x1mode_to_stretch,
                               "kwargs":{"pmode_h":"@x1mode", "mass":"@mass"}
                          },           
                    "magabs": {"func": magnitude.standardisation_brokenalpha,
                        "kwargs": {"x1": "@x1", "x1mode":"@x1mode",
                                    "c": "@c", "isup":'@prompt',
                                    "alpha_low":-0.23, "alpha_high":-0.07, 
                                    "mabs":-19.35, "sigmaint":0.1, 
                                    "gamma":0.2, "x1ref":-0.5,
                                  }
                            },
                    }


cluster_prompt_model = {"rcluster": {"func": lss.get_cluster_radius, "kwargs":{}},
                        "prompt": {"func": lss.get_cluster_prompt, "kwargs":{"radius":"@rcluster",
                                                                 "redshift":"@z"}}
                        }
