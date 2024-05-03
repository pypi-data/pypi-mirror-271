import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.linear_model import LinearRegression

class appproximateStraightLineMechanism1:
    def __init__(self, vars=None):
        self.θ_0 = 0 # default value
        self.θ_0_increment = 0
        self.vertical_threshold = 0.01
        self.theta_values = np.linspace(-np.pi/2, 1.5 * np.pi, 400)
        self.fig = self.figH = self.figS = None
        self.axs = None
        if vars is not None:
            self.setVars(vars)
        if self.plotType == "locus":
          self.plotAll({"curve":True, "curvature":True})
        elif self.plotType =="values":
          self.plotallvalues({"s":True, "h":True, "curvature":True, "fractional":True})

    def setVars(self, vars):
        self.__dict__.update(vars)

    def curve_parametric(self):
        θ_0 = self.θ_0 + self.θ_0_increment
        theta = self.theta_values
        R = self.R
        r = self.R * self.f
        a = self.a
        x = R * np.cos(theta) + r * np.cos((1 + a) * theta + math.radians(θ_0))
        y = R * np.sin(theta) + r * np.sin((1 + a) * theta + math.radians(θ_0))
        return x, y

    def curvature_parametric(self, R, f, a, θ_0_increment=False):
        θ_0 = self.θ_0 + (self.θ_0_increment if θ_0_increment == False else θ_0_increment)
        theta = self.theta_values
        r = R * f
        dx_dtheta = -R * np.sin(theta) - r * (1 + a) * np.sin((1 + a) * theta + math.radians(θ_0))
        dy_dtheta = R * np.cos(theta) + r * (1 + a) * np.cos((1 + a) * theta + math.radians(θ_0))
        d2x_dtheta2 = -R * np.cos(theta) - r * (1 + a)**2 * np.cos((1 + a) * theta + math.radians(θ_0))
        d2y_dtheta2 = -R * np.sin(theta) - r * (1 + a)**2 * np.sin((1 + a) * theta + math.radians(θ_0))
        curvature = (dx_dtheta * d2y_dtheta2 - dy_dtheta * d2x_dtheta2) / (dx_dtheta**2 + dy_dtheta**2)**(3/2)
        return dx_dtheta, dy_dtheta, curvature

    def __plotCurve(self, plot):
        self.setRequiredTheta0()

        x_curve, y_curve = self.curve_parametric()
        longest_segment = self.get_longest_straight_line()
        plot.clear()
        plot.plot(x_curve, y_curve)
        plot.plot(x_curve[longest_segment], y_curve[longest_segment], color='green', label='Longest Segment', linewidth=8)
        plot.set_title(rf'Output Locus(θ$_0$: {self.getRequiredTheta0()}°, h:{self.getdH():.4f}, s:{self.getdS():.4f}, l:{self.getStraightSectionFraction():.2f}%)')
        plot.set_aspect('equal')

    def plotStraightSection(self, plot):
        # the straight line section
        x_straight, y_reg = self.expected_straight_line()
        plot.plot(x_straight, y_reg, color='red', linestyle='--', label='Linear Regression')
    def plotCurvature(self, plot):
        _, _, curvature = self.curvature_parametric(self.R, self.f, self.a)
        theta_degrees = np.degrees(self.theta_values)
        longest_segment = self.get_longest_straight_line()
        # curvature and straight segment
        plot.clear()
        plot.plot(theta_degrees, curvature)
        plot.set_title(f'Plot of Curvature(max:{self.getmaxCurvature():.6f})')

        plot.scatter(theta_degrees[longest_segment], curvature[longest_segment], color='red')
        # plot.legend()
    def plotdS(self, plot):
        pass
    def plotdH(self, plot):
        pass
    def plotmaxCurvature(self, plot):
        pass
    def plotStraightSectionFraction(self, plot):
        pass

    def plotAll(self, options={}):
        numGraphs = len(options.keys())
        numGraphs = numGraphs if numGraphs > 1 else numGraphs + 1
        fig = axs = None

        if self.fig == None:
          fig, axs = plt.subplots(1, numGraphs, figsize=(12, 6))
          self.fig = fig
          self.axs = axs
        else:
          fig = self.fig
          axs = self.axs
        self.fig.suptitle(f"Straight Line Generator (R:{self.R:.2f}, f:{self.f:.2f}, a:{self.a}, curvature:{self.curvature_threshold:.2f})")
        axsIndex = 0
        for key in options:
          if key == "curve":
            self.__plotCurve(axs[axsIndex])
            self.plotStraightSection(axs[axsIndex])
            axsIndex+=1
          if key == "curvature":
            self.plotCurvature(axs[axsIndex])
            axsIndex+=1
          if key == "curvatures":
            pass

        plt.tight_layout()
        # plt.show()
    def updateAllPlot(self, frame, numFrames, updateVar, plotOptions):
        for var_name, var_data in updateVar.items():
          if var_name == 'R':
              R = var_data['min'] + (var_data['max'] - var_data['min']) * frame / numFrames
              self.R = R
              self.fig.suptitle(f"Straight Line Generator (R) (R:{self.R:.2f}, f:{self.f:.2f}, a:{self.a}, curvature:{self.curvature_threshold:.2f})")
          elif var_name == 'f':
              f = var_data['min'] + (var_data['max'] - var_data['min']) * frame / numFrames
              self.f = f
              self.fig.suptitle(f"Straight Line Generator (f) (R:{self.R:.2f}, f:{self.f:.2f}, a:{self.a}, curvature:{self.curvature_threshold:.2f})")
          elif var_name == 'a':
              a = int(var_data['min'] + (var_data['max'] - var_data['min']) * frame / numFrames)
              self.a = a
              self.fig.suptitle(f"Straight Line Generator (a) (R:{self.R:.2f}, f:{self.f:.2f}, a:{self.a}, curvature:{self.curvature_threshold:.2f})")
          elif var_name == 'curvature_threshold':
              curvature_threshold = var_data['min'] + (var_data['max'] - var_data['min']) * frame / numFrames
              self.curvature_threshold = curvature_threshold
              self.fig.suptitle(f"Straight Line Generator (curvature) (R:{self.R:.2f}, f:{self.f:.2f}, a:{self.a}, curvature:{self.curvature_threshold:.2f})")
          break # do for only the first

        axsIndex = 0
        for key in plotOptions:
          if key == "curve":
            self.__plotCurve(self.axs[axsIndex])
            self.plotStraightSection(self.axs[axsIndex])
            axsIndex+=1
          if key == "curvature":
            self.plotCurvature(self.axs[axsIndex])
            axsIndex+=1
          if key == "curvatures":
            pass




    def expected_straight_line(self):
        longest_segment = self.get_longest_straight_line()
        x_straight = self.curve_parametric()[0][longest_segment]
        y_straight = self.curve_parametric()[1][longest_segment]
        ret_x=ret_y = None
        # Check if the line is nearly vertical because linear regression does not work so well with vertical lines
        if len(x_straight) == 0:
          return (0,0)
        if np.abs(np.max(x_straight) - np.min(x_straight)) < self.vertical_threshold:  # Adjust threshold as needed
            # Handle vertical line by using a fixed x-coordinate
            x_value = np.mean(x_straight)  # You can choose mean, median, or another central value
            x_straight[:] = x_value
            ret_x = x_straight
            ret_y = y_straight
            self.slope = np.Infinity
        # Fit linear regression to the straight section (for non-vertical lines)
        else:
            reg = LinearRegression().fit(x_straight[:, np.newaxis], y_straight)
            y_reg = reg.predict(x_straight[:, np.newaxis])
            ret_x = x_straight
            ret_y = y_reg
            # return (x_straight, y_reg)
            slope = (ret_y[-1] - ret_y[0]) / (ret_x[-1] - ret_x[0])
            self.slope = slope
            angle_radians = np.arctan(slope)
            self.lineAngle = np.degrees(angle_radians)
            # print(self.lineAngle)

        return (ret_x, ret_y)

    def get_longest_straight_line(self):
      _,_,curvature = self.curvature_parametric(self.R, self.f, self.a)
      straight_line_indices = np.where(np.abs(curvature) < self.curvature_threshold)[0]
      segments = np.split(straight_line_indices, np.where(np.diff(straight_line_indices) != 1)[0] + 1)

      # Check if there are segments both at the beginning and end
      if segments and len(segments) > 1 and segments[-1][-1] == len(curvature) - 1 and segments[0][0] == 0:
          # Combine the segments into the first segment
          combined_segment = np.concatenate((segments[-1], segments[0]))
          # Remove the last segment
          segments.pop()
          # Replace the first segment with the combined segment
          segments[0] = combined_segment

      longest_segment = max(segments, key=len)
      return longest_segment

    def setRequiredTheta0(self):
      self.θ_0_increment = self.getRequiredθ_0_increment()
    def getRequiredTheta0(self):
      # θ_0_increment = self.getRequiredθ_0_increment() # because this function will be called after setRequiredTheta0
      return self.θ_0_increment + self.θ_0

    def middle_of_line_at_0(self):
      count=0;
      θ_0_increment = 0
      θ_0_increment_interval = 1
      _,_,curvature = self.curvature_parametric(self.R, self.f, self.a, θ_0_increment)
      while count < len(curvature)//θ_0_increment_interval: # mat
        θ_0_increment += θ_0_increment_interval
        _,_,curvature = self.curvature_parametric(self.R, self.f, self.a, θ_0_increment)
        straight_line_indices = np.where(np.abs(curvature) < self.curvature_threshold)[0]
        segments = np.split(straight_line_indices, np.where(np.diff(straight_line_indices) != 1)[0] + 1)

        if segments and len(segments) > 1 and segments[-1][-1] == len(curvature) - 1 and segments[0][0] == 0:
          if len(segments[0]) == len(segments[-1]):
              combined_segment = np.concatenate((segments[-1], segments[0]))
              # Remove the last segment
              segments.pop()
              # Replace the first segment with the combined segment
              segments[0] = combined_segment
              longest_segment = max(segments, key=len)
              try:
                is_first_segment_longest = (longest_segment == segments[0]).all()
                if is_first_segment_longest:
                  break
              except:
                pass
        count += 1
      return θ_0_increment

    def getRequiredθ_0_increment(self):
      θ_0_increment = 0.1
      longest_segment = self.get_longest_straight_line()
      x_straight = self.curve_parametric()[0][longest_segment]
      y_straight = self.curve_parametric()[1][longest_segment]
      ret_x=ret_y = None
      if len(x_straight) == 0:
        return 0
      # Check if the line is nearly vertical because linear regression does not work so well with vertical lines
      # print(x_straight, np.abs(np.max(x_straight) - np.min(x_straight)), self.vertical_threshold)
      if np.abs(np.max(x_straight) - np.min(x_straight)) < self.vertical_threshold:  # Adjust threshold as needed
          x_value = np.mean(x_straight)  # You can choose mean, median, or another central value
          x_straight[:] = x_value
          ret_x = x_straight
          ret_y = y_straight
          self.slope = np.Infinity
          if y_straight[0] < y_straight[-1]:
            θ_0_increment = 90
          else:
            θ_0_increment = -90
      else:
          θ_0_increment = self.middle_of_line_at_0()

      return θ_0_increment
    def getdH(self): # get height
      self.setRequiredTheta0()
      longest_segment = self.get_longest_straight_line()
      x_straight = self.curve_parametric()[0][longest_segment]
      y_straight = self.curve_parametric()[1][longest_segment]
      if len(y_straight) == 0:
        self.dh = 0
        return 0
      dh = np.max(y_straight) - np.min(y_straight)
      self.dh = dh
      return dh
    def getdS(self):
      self.setRequiredTheta0()
      longest_segment = self.get_longest_straight_line()
      x_straight = self.curve_parametric()[0][longest_segment]
      if len(x_straight) == 0:
        self.ds = 0
        return 0
      ds = x_straight[-1] - x_straight[0] if x_straight[-1] > x_straight[0] else -x_straight[-1] + x_straight[0] if x_straight[-1] < x_straight[0] else 0
      # ds = x_straight[-1] - x_straight[0]
      self.ds = ds
      return ds
    def getStraightSectionFraction(self):
      self.setRequiredTheta0()
      longest_segment = self.get_longest_straight_line()
      x_straight = self.curve_parametric()[0][longest_segment]
      if len(x_straight) == 0:
        self.straightFraction = 0
        return 0
      fraction = (len(x_straight)/len(self.curve_parametric()[0]))*100
      fraction = round(fraction, 2)
      self.straightFraction = fraction
      return fraction
    def getmaxCurvature(self):
      self.setRequiredTheta0()
      _, _, curvature = self.curvature_parametric(self.R, self.f, self.a)
      maxCurvature = np.max(curvature)
      self.maxCurvature = maxCurvature
      return maxCurvature
    def plotallvalues(self, options):
      # "s":True, "h":True, "curvature":True, "fractional":True

      for key in options:
        if key == "s":
          self.plotSForWholeRange()
        if key == "h":
          self.plotHForWholeRange()
        if key == "curvatures":
          pass
        if key == "fractiona":
          pass

      plt.tight_layout()
      pass
    def plotSForWholeRange(self):
      numGraphs = 4
      fig = axs = None
      if self.figS == None:
        fig, axs = plt.subplots(1, numGraphs, figsize=(12, 6))
        self.figS = fig
        self.axsS = axs
      else:
        fig = self.figS
        axs = self.axsS

      ### Plot for all R
      self.figS.suptitle(f"S for whole range (R:{self.R:.2f}, f:{self.f:.2f}, a:{self.a}, curvature:{self.curvature_threshold:.2f})")
      # Plot of R
      R_values = np.linspace(0, 10, 100)
      dS_values = []

      for R in R_values:
          # Update R value
          self.R = R
          # Calculate dS for the current R
          dS = self.getdS()
          dS_values.append(dS)

      # Plot dS values against R values
      axs[0].plot(R_values, dS_values)
      axs[0].set_xlabel('R')
      axs[0].set_ylabel('S')
      axs[0].set_title('S vs. R')

      # plot of f
      f_values = np.linspace(0, 1, 100)
      dS_values = []

      for f in f_values:
          # Update R value
          self.f = f
          # Calculate dS for the current R
          dS = self.getdS()
          dS_values.append(dS)

      # Plot dS values against f values
      axs[1].plot(f_values, dS_values)
      axs[1].set_xlabel('f')
      axs[1].set_ylabel('S')
      axs[1].set_title('S vs. f')


      # plot of a
      a_values = np.linspace(-10, 10, 21)
      dS_values = []

      for a in a_values:
          # Update R value
          self.a = a
          # Calculate dS for the current R
          dS = self.getdS()
          dS_values.append(dS)

      # Plot dS values against R values
      axs[2].plot(a_values, dS_values)
      axs[2].set_xlabel('a')
      axs[2].set_ylabel('S')
      axs[2].set_title('S vs. a')

      ## curvature_threshold
      c_values = np.linspace(0, 3, 100)
      dS_values = []

      for c in c_values:
          # Update R value
          self.curvature_threshold = c
          # Calculate dS for the current R
          dS = self.getdS()
          dS_values.append(dS)

      # Plot dS values against R values
      axs[3].plot(c_values, dS_values)
      axs[3].set_xlabel('curvature_threshold')
      axs[3].set_ylabel('S')
      axs[3].set_title('S vs. curvature_threshold')

      plt.tight_layout()
    def plotHForWholeRange(self):
        numGraphs = 4
        fig = axs = None
        if self.figH == None:
            fig, axs = plt.subplots(1, numGraphs, figsize=(12, 6))
            self.figH = fig
            self.axsH = axs
        else:
            fig = self.figH
            axs = self.axsH

        ### Plot for all R
        self.figH.suptitle(f"H for whole range (R:{self.R:.2f}, f:{self.f:.2f}, a:{self.a}, curvature:{self.curvature_threshold:.2f})")
        # Plot of R
        R_values = np.linspace(0, 10, 100)
        dH_values = []

        for R in R_values:
            # Update R value
            self.R = R
            # Calculate dH for the current R
            dH = self.getdH()
            dH_values.append(dH)

        # Plot dH values against R values
        axs[0].plot(R_values, dH_values)
        axs[0].set_xlabel('R')
        axs[0].set_ylabel('H')
        axs[0].set_title('H vs. R')

        # plot of f
        f_values = np.linspace(0, 1, 100)
        dH_values = []

        for f in f_values:
            # Update f value
            self.f = f
            # Calculate dH for the current f
            dH = self.getdH()
            dH_values.append(dH)

        # Plot dH values against f values
        axs[1].plot(f_values, dH_values)
        axs[1].set_xlabel('f')
        axs[1].set_ylabel('H')
        axs[1].set_title('H vs. f')


        # plot of a
        a_values = np.linspace(-10, 10, 21)
        dH_values = []

        for a in a_values:
            # Update a value
            self.a = a
            # Calculate dH for the current a
            dH = self.getdH()
            dH_values.append(dH)

        # Plot dH values against a values
        axs[2].plot(a_values, dH_values)
        axs[2].set_xlabel('a')
        axs[2].set_ylabel('H')
        axs[2].set_title('H vs. a')

        ## curvature_threshold
        c_values = np.linspace(0, 3, 100)
        dH_values = []

        for c in c_values:
            # Update curvature_threshold value
            self.curvature_threshold = c
            # Calculate dH for the current curvature_threshold
            dH = self.getdH()
            dH_values.append(dH)

        # Plot dH values against curvature_threshold values
        axs[3].plot(c_values, dH_values)
        axs[3].set_xlabel('curvature_threshold')
        axs[3].set_ylabel('H')
        axs[3].set_title('H vs. curvature_threshold')

        plt.tight_layout()