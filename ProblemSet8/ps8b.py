# Problem Set 8: Simulating the Spread of Disease and Virus Population Dynamics 

import numpy
import random
import pylab
from ps8b_precompiled_27 import *
# For debug
random.seed(0)
''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 2
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        # TODO
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        # TODO
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        # TODO
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """

        # TODO
        return random.random() < self.clearProb

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.getMaxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """

        # TODO
        rep_prob = self.getMaxBirthProb() * (1 - popDensity)
        if random.random() < rep_prob:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException()




class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        # TODO
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        # TODO
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        # TODO
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        # TODO  
        return len(self.viruses)      


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        current_viruses = self.viruses[:]
        cur_popDensity = float(self.getTotalPop()) / self.maxPop

        for virus in current_viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                try:
                    self.viruses.append(virus.reproduce(cur_popDensity))
                except NoChildException:
                    pass

        return self.getTotalPop()



#
# PROBLEM 3
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    # TODO

    # Initialize variables
    timesteps = 300
    viruses = []
    total_each_timesteps = [0 for t in range(timesteps)]
    average_size = [0 for t in range(timesteps)]
    for i in range(numViruses):
        viruses.append(SimpleVirus(maxBirthProb, clearProb))

    # Begin trial
    for i in range(numTrials):
        p = Patient(viruses[:], maxPop)
        time = 0
        while time < timesteps:
            vir_pop = p.update()
            total_each_timesteps[time] += vir_pop
            time += 1

    # Calculate the average size of virus population in
    # patient correspond to each timesteps
    for t in range(timesteps):
        average_size[t] = float(total_each_timesteps[t]) / numTrials
    
    # Draw the plot
    pylab.figure(1)
    pylab.plot([time for time in range(timesteps)], average_size)
    pylab.title('Simple simulation')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.legend()
    pylab.show()






#
# PROBLEM 4
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        # TODO
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        # TODO
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb
        # TODO

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        # TODO
        return self.resistances.get(drug, False)


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.getMaxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb, clearProb, and mutProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        # TODO

        # Test virus resistant
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()

        rep_prob = self.getMaxBirthProb() * (1 - popDensity)
        new_resistances = {}

        if random.random() < rep_prob:
            # Creat new resistances for child
            for key in self.resistances:
                if random.random() < self.mutProb:
                    new_resistances[key] = not self.resistances[key]
                else:
                    new_resistances[key] = self.resistances[key]

            return ResistantVirus(self.maxBirthProb, self.clearProb,
                                  new_resistances, self.mutProb)
        else:
            raise NoChildException()


            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        # TODO
        Patient.__init__(self, viruses, maxPop)
        self.drugs = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        # TODO
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        # TODO
        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        # TODO
        resist_pop = 0
        is_resi = False
        for virus in self.viruses:
            for drug in drugResist:
                if drug in virus.getResistances():
                    if virus.isResistantTo(drug):
                        is_resi = True
                    else:
                        is_resi = False
                        break
                else:
                    is_resi = False
                    break
            if is_resi:
                resist_pop += 1
            
        return resist_pop




    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # TODO
        current_viruses = self.viruses[:]
        cur_popDensity = float(self.getTotalPop()) / self.maxPop

        for virus in current_viruses:
            if virus.doesClear():
                self.viruses.remove(virus)
            else:
                try:
                    self.viruses.append(virus.reproduce(cur_popDensity, self.drugs))
                except NoChildException:
                    pass

        return self.getTotalPop()

#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)b
    
    """

    # TODO
    timesteps = 300
    # Data Set
    total_virus_pop = [0 for t in range(timesteps)]
    guttagonol_virus_pop = [0 for t in range(timesteps)]
    average_size_virus_pop = [0 for t in range(timesteps)]
    average_size_guttagonol = [0 for t in range(timesteps)]
    # Initailize viruse
    viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for i in range(numViruses)]
   
    # Begin Trial
    for i in range(numTrials):
        p = TreatedPatient(viruses[:], maxPop)
        time = 0
        while time < 150:
            vir_pop = p.update()
            total_virus_pop[time] += vir_pop
            guttagonol_virus_pop[time] += p.getResistPop(['guttagonol'])
            time += 1
        # Additional timesteps
        p.addPrescription('guttagonol')
        while time < timesteps: 
            vir_pop = p.update()
            total_virus_pop[time] += vir_pop
            guttagonol_virus_pop[time] += p.getResistPop(['guttagonol'])
            time += 1

    for t in range(timesteps):
        average_size_virus_pop[t] = float(total_virus_pop[t]) / float(numTrials)
        average_size_guttagonol[t] = float(guttagonol_virus_pop[t]) / float(numTrials)

    print average_size_virus_pop
    print average_size_guttagonol

    # Draw the plot
    pylab.figure(1)
    x = [time for time in range(timesteps)]
    pylab.plot(x, average_size_virus_pop, label='total virus population')
    pylab.plot(x, average_size_guttagonol, label='guttagonol-resistant virus population')
    pylab.title('SIMULATION WITH A DRUG')
    pylab.xlabel('Time Steps')
    pylab.ylabel('Virus Population')
    pylab.legend()
    pylab.show()
    

if __name__ == '__main__':
    simulationWithDrug(100, 1000, 0.1, 0.05, {"guttagonol": False}, 0.05, 100)
    #simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
    #simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
    #simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
    #simulationWithoutDrug(100, 1000, 0.1, 0.05, 100)
