import time
import random
class FlowMeter():
  ERROR_CORRECTION = 1.351 *2
  PINTS_IN_A_LITER = 2.11338
  OUNCES_IN_A_LITER = 33.814
  SECONDS_IN_A_MINUTE = 60
  MS_IN_A_SECOND = 1000.0
  displayFormat = 'metric'
  beverage = 'beer'
  enabled = True
  clicks = 0
  lastClick = 0
  clickDelta = 0
  hertz = 0.0
  flow = 0 # in Liters per second
  thisPour = 0.0 # in Liters
  lastPour = 0.0
  lasterPour = 0.0
  totalPour = 0.0 # in Liters

  def __init__(self, displayFormat, beverage):
    self.displayFormat = displayFormat
    self.beverage = beverage
    self.clicks = 0
    self.lastClick = int(time.time() * FlowMeter.MS_IN_A_SECOND)
    self.clickDelta = 0
    self.hertz = 0.0
    self.flow = 0.0
    self.thisPour = 0.0
    self.lastPour = 0.0
    self.lasterPour = 0.0
    self.totalPour = 0.0
    self.enabled = True

  def update(self, currentTime):
    self.clicks += 1
    # get the time delta
    self.clickDelta = max((currentTime - self.lastClick), 1)
    # calculate the instantaneous speed
    if (self.enabled == True and self.clickDelta < 1000):
      self.hertz = FlowMeter.MS_IN_A_SECOND / self.clickDelta
      self.flow = self.hertz / (FlowMeter.SECONDS_IN_A_MINUTE * 7.5)  # In Liters per second
      instPour = self.flow * (self.clickDelta / FlowMeter.MS_IN_A_SECOND)  
      instPour *= FlowMeter.ERROR_CORRECTION
      self.thisPour += instPour
      self.totalPour += instPour
    # Update the last click
    self.lastClick = currentTime

  def getBeverage(self):
    return str(random.choice(self.beverage))

  def getFormattedClickDelta(self):
     return str(self.clickDelta) + ' ms'
  
  def getFormattedHertz(self):
     return str(round(self.hertz,1)) + ' Hz'
  
  def getFormattedFlow(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.flow,1)) + ' L/s'
    elif(self.displayFormat == 'imp'):
      return str(round(self.flow * FlowMeter.OUNCES_IN_A_LITER,1)) + ' OZ/s'
    else:
      return str(round(self.flow * FlowMeter.PINTS_IN_A_LITER,1)) + ' pints/s'
  
  def getFormattedThisPour(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.thisPour,1)) + ' L'
    elif(self.displayFormat == 'imp'):
      return str(round(self.thisPour * FlowMeter.OUNCES_IN_A_LITER,1)) + ' OZ'
    else:
      return str(round(self.thisPour * FlowMeter.PINTS_IN_A_LITER,1)) + ' pints'
  
  def getFormattedLastPour(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.lastPour,1)) + ' L'
    elif(self.displayFormat == 'imp'):
      return str(round(self.lastPour * FlowMeter.OUNCES_IN_A_LITER,1)) + ' OZ'
    else:
      return str(round(self.lastPour * FlowMeter.PINTS_IN_A_LITER,1)) + ' pints'

  def getFormattedLasterPour(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.lasterPour,1)) + ' L'
    elif(self.displayFormat == 'imp'):
      return str(round(self.lasterPour * FlowMeter.OUNCES_IN_A_LITER,1)) + ' OZ'
    else:
      return str(round(self.lasterPour * FlowMeter.PINTS_IN_A_LITER,1)) + ' pints'
      
  def getFormattedTotalPour(self):
    if(self.displayFormat == 'metric'):
      return str(round(self.totalPour,1)) + ' L'
    elif(self.displayFormat == 'imp'):
      return str(round(self.totalPour * FlowMeter.OUNCES_IN_A_LITER,1)) + ' OZ'
    else:
      return str(round(self.totalPour * FlowMeter.PINTS_IN_A_LITER,1)) + ' pints'

  def clear(self):
    self.lasterPour = self.lastPour;
    self.lastPour = self.thisPour;
    self.thisPour = 0;
    
