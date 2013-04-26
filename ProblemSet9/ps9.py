# 6.00 Problem Set 9

import numpy
import random
import pylab
from ps8b_precompiled_27 import *



#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    
    # TODO

    # Initialize variables.
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False}
    mutProb = 0.005
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(100)]
    times_cond = [300, 150, 75, 0]


    # Store plot datas

    times_total_virus_pop = {300: [0] * 450, 150: [0] * 300, 75: [0] * 225, 0: [0] * 150}
    times_guttagonol_virus_pop = {300: [0] * 450, 150: [0] * 300, 75: [0] * 225, 0: [0] * 150}
    times_average_size_virus_pop = {300: [0] * 450, 150: [0] * 300, 75: [0] * 225, 0: [0] * 150}
    times_average_size_guttagonol = {300: [0] * 450, 150: [0] * 300, 75: [0] * 225, 0: [0] * 150}


    # Store histogram datas
    times_pops = {300: [0] * numTrials, 150: [0] * numTrials,
                  75: [0] * numTrials, 0: [0] * numTrials}

    # Begin each trial
    for time_cond in times_cond:
        total_timesteps = time_cond + 150
        for i in range(numTrials):
            p = TreatedPatient(viruses[:], maxPop)
            time = 0
            while time < time_cond:
                vir_pop = p.update()
                times_total_virus_pop[time_cond][time] += vir_pop
                times_guttagonol_virus_pop[time_cond][time] += p.getResistPop(['guttagonol'])
                time += 1
        # Additional timesteps
            p.addPrescription('guttagonol')
            while time < total_timesteps: 
                vir_pop = p.update()
                times_total_virus_pop[time_cond][time] += vir_pop
                times_guttagonol_virus_pop[time_cond][time] += p.getResistPop(['guttagonol'])
                time += 1
            times_pops[time_cond][i] = p.getTotalPop()

    # for t_c in times_cond:
    #     for t in range(t_c + 150):
    #         times_average_size_virus_pop[t_c][t] = float(times_total_virus_pop[t_c][t]) / float(numTrials)
    #         times_average_size_guttagonol[t_c][t] = float(times_guttagonol_virus_pop[t_c][t]) / float(numTrials)


    # for t_c in times_cond:        
    #     pylab.figure('plot delays %s' % t_c)
    #     x = [time for time in range(t_c + 150)]
    #     pylab.plot(x, times_average_size_virus_pop[t_c], label='total virus population')
    #     pylab.plot(x, times_average_size_guttagonol[t_c], label='guttagonol-resistant virus population')
    #     pylab.title('SIMULATION WITH A DRUG')
    #     pylab.xlabel('Time Steps')
    #     pylab.ylabel('Virus Population')
    #     pylab.legend()


    # for t_c in times_cond:
    #     pylab.figure('histogram delays %s' % t_c)
    #     pylab.hist(times_pops[t_c], bins=50)
    #     pylab.xlabel('Total virus population')
    #     pylab.ylabel('Number of trials')
    
    # pylab.show()

    # calculating cutred percentage 
    # for time in times_cond:
    #     count = 0
    #     for i in range(numTrials):
    #         if times_pops[time][i] < 50:
    #             count += 1
    #     print 'time :', time
    #     print 'less than 50:', count
    #     print 'pre: ', float(count) / numTrials * 100





#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """
    # TODO
    maxPop = 1000
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False, 'grimpex': False}
    mutProb = 0.005
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(100)]
    conditions = [300, 150, 75, 0]

    # Store sim data
    final_virus_pops = {300: [0] * numTrials, 150: [0] * numTrials,
                        75: [0] * numTrials, 0: [0] * numTrials}

    total_virus_pop = {300: [0] * 600, 150: [0] * 450, 75: [0] * 375, 0: [0] * 300}
    guttagonol_virus_pop = {300: [0] * 600, 150: [0] * 450, 75: [0] * 375, 0: [0] * 300}
    grimpex_virus_pop = {300: [0] * 600, 150: [0] * 450, 75: [0] * 375, 0: [0] * 300}
    average_size_virus_pop = {300: [0] * 600, 150: [0] * 450, 75: [0] * 375, 0: [0] * 300}
    average_size_guttagonol = {300: [0] * 600, 150: [0] * 450, 75: [0] * 375, 0: [0] * 300}
    average_size_grimpex = {300: [0] * 600, 150: [0] * 450, 75: [0] * 375, 0: [0] * 300}

    # Begin trial
    for cond in conditions:
        total_timesteps = 150 + cond + 150
        second_timesteps = 150 + cond
        for i in range(numTrials):
            time = 0
            p = TreatedPatient(viruses[:], maxPop)

            # For each trial, run the first 150 time steps 
            # before administering guttagonol to the patient
            while time < 150:
                vir_pop = p.update()
                # total_virus_pop[cond][time] += vir_pop
                # guttagonol_virus_pop[cond][time] += p.getResistPop(['guttagonol'])
                # grimpex_virus_pop[cond][time] += p.getResistPop(['grimpex'])
                time += 1
            
            # add guttagonol, run simulation for cond time steps
            # before administering a second drug grimpex
            p.addPrescription('guttagonol')
            while time < second_timesteps:
                vir_pop = p.update()
                # total_virus_pop[cond][time] += vir_pop
                # guttagonol_virus_pop[cond][time] += p.getResistPop(['guttagonol'])
                # grimpex_virus_pop[cond][time] += p.getResistPop(['grimpex'])
                time += 1
            
            # add second drug grimpex
            # run simulation for another 150 time steps
            p.addPrescription('grimpex')
            while time < total_timesteps:
                vir_pop = p.update()
                # total_virus_pop[cond][time] += vir_pop
                # guttagonol_virus_pop[cond][time] += p.getResistPop(['guttagonol'])
                # grimpex_virus_pop[cond][time] += p.getResistPop(['grimpex'])
                time += 1
            final_virus_pops[cond][i] = p.getTotalPop()


    # for cond in conditions:
    #     for t in range(150 + cond + 150):
    #         average_size_virus_pop[cond][t] = float(total_virus_pop[cond][t]) / float(numTrials)
    #         average_size_guttagonol[cond][t] = float(guttagonol_virus_pop[cond][t]) / float(numTrials)
    #         average_size_grimpex[cond][t] = float(grimpex_virus_pop[cond][t]) / float(numTrials)

    # # Draw the plot
    # for cond in conditions:        
    #     pylab.figure('two durg plot delays %s' % cond)
    #     x = [time for time in range(150 + cond + 150)]
    #     pylab.plot(x, average_size_virus_pop[cond], label='total virus population')
    #     pylab.plot(x, average_size_guttagonol[cond], label='guttagonol-resistant virus population')
    #     pylab.plot(x, average_size_grimpex[cond], label='grimpex-resistant virus population')
    #     pylab.title('SIMULATION WITH A DRUG')
    #     pylab.xlabel('Time Steps')
    #     pylab.ylabel('Virus Population')
    #     pylab.legend()


    # Draw the histogram
    for cond in conditions:
        pylab.figure('histogram delays %s' % cond)
        pylab.hist(final_virus_pops[cond], bins=50)
        pylab.xlabel('Final virus population')
        pylab.ylabel('Number of trials')

    pylab.show()
 



if __name__ == '__main__':
    # simulationDelayedTreatment(500)
    simulationTwoDrugsDelayedTreatment(500)