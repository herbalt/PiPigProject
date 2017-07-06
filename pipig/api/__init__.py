from flask_restplus import Api

api = Api(version='1.0', title='PiPig Api',
          description='PiPig is an application to control and review the conditions of a Charcuterie Fridge.'
                      ' PiPig connects three core components {sensors, datapoints, appliances} together into Recipes'
                      ' to run to control the environmental conditions of the fridge')



