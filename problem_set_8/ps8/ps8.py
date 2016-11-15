# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

'''
Begin helper code
'''

# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

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
# PROBLEM 1
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

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        # generate a random number
        prob = random.random()
        return prob < self.clearProb

    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

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

        prob = random.random()
        if prob < self.maxBirthProb * (1 - popDensity):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException


class SimplePatient(object):
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

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getTotalPop(self):

        """
        Gets the current total virus population.
        returns: The total virus population (an integer)
        """

        return len(self.viruses)

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.
        - The current population density is calculated. This population density
          value is used until the next call to update()
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """

        # determines survival of virus particles
        v_tmp = []
        for v in self.viruses:
            if v.doesClear():
                pass

            else:
                v_tmp.append(v)

        self.viruses = v_tmp

        # determines reproduction of virus particles
        popDensity = len(self.viruses) / float(self.maxPop)
        # print popDensity
        for v in self.viruses:
            try:
                v_tmp.append(v.reproduce(popDensity))
            except NoChildException:
                pass

        self.viruses = v_tmp

        return len(self.viruses)


#
# PROBLEM 2
#
def simulationWithoutDrug():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.
    """

    # create list of viruses
    n_viruses = 100
    viruses = []
    for i in range(0, n_viruses):
        viruses.append(SimpleVirus(0.1, 0.05))

    # instantiate patient
    maxPop = 1000
    patient = SimplePatient(viruses, maxPop)

    # run simulation
    t_steps = 300
    v_pop = [n_viruses]
    for t in range(0, t_steps):
        v_pop.append(patient.update())

    # pylab.plot(v_pop)
    # pylab.show()
    return v_pop

'''
End helper code
'''

#
# PROBLEM 1
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
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb

    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        if drug in self.resistances:
            return self.resistances[drug]
        else:
            return False

    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        reproduce_flag = True

        # print activeDrugs
        for d in activeDrugs:
            # print d
            # print self.resistances

            if d in self.resistances:
                if self.resistances[d]:
                    pass
                else:
                    reproduce_flag = False
            else:
                # the virus will not reproduce
                reproduce_flag = False


        rnd1 = random.random()
        if (reproduce_flag is True) & (rnd1 < self.maxBirthProb * (1 - popDensity)):

            new_resistances = {}

            # determine whether the virus acquires or doesn't new resistances
            for r in self.resistances:
                rnd2 = random.random()
                if self.resistances[r] is True:
                    if rnd2 > self.mutProb:
                        new_resistances[r] = True
                    else:
                        new_resistances[r] = False
                else:
                    if rnd2 < self.mutProb:
                        new_resistances[r] = True
                    else:
                        new_resistances[r] = False

            return ResistantVirus(self.maxBirthProb, self.clearProb,
                                  new_resistances,self.mutProb)

        else:

            raise NoChildException


class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.drugs = []

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # should not allow one drug being added to the list multiple times
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        count_resistant = 0

        if len(drugResist) > 0:

            for virus in self.viruses:

                resist_flag = True

                for d in drugResist:
                    if virus.isResistantTo(d) is False:
                        resist_flag = False

                if resist_flag is True:
                    count_resistant += 1

        return count_resistant

    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """

        # determine virus survival
        new_viruses = []
        # print len(self.viruses)

        for v in self.viruses:
            if v.doesClear() is False:
                new_viruses.append(v)

        self.viruses = new_viruses
        # print len(self.viruses)
        # calculate population density
        popDensity = len(new_viruses) / float(self.maxPop)

        # determine reproduction
        for v in self.viruses:
            try:
                new_viruses.append(v.reproduce(popDensity,self.drugs))
            except NoChildException:
                pass

        self.viruses = new_viruses

        # print len(self.viruses)

        return len(self.viruses)

#
# PROBLEM 2
#

def simulationWithDrug(t):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """

    # make viruses
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol':False}
    mutProb = 0.005

    viruses = []
    for i in range(0, 100):
        viruses.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))

    maxPop = 1000
    patient = Patient(viruses, maxPop)

    output_tot = []
    output_res = []

    # run the first t steps
    for j in range(0, t):
        output_tot.append(patient.update())
        output_res.append(patient.getResistPop(['guttagonol']))

    # add the drug then run again for 150
    patient.addPrescription('guttagonol')
    for j in range(0, 150):
        output_tot.append(patient.update())
        output_res.append(patient.getResistPop(patient.getPrescriptions()))


    return output_tot, output_res
#
# PROBLEM 3
#        

def simulationDelayedTreatment(t):

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """

    # make viruses
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol':False}
    mutProb = 0.005

    viruses = []
    for i in range(0, 100):
        viruses.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))

    maxPop = 1000
    patient = Patient(viruses, maxPop)

    output_tot = []
    output_res = []

    # run the first t steps
    for j in range(0, t):
        output_tot.append(patient.update())
        output_res.append(patient.getResistPop(['guttagonol']))

    # add the drug then run again for 150
    patient.addPrescription('guttagonol')
    for j in range(0, 150):
        output_tot.append(patient.update())
        output_res.append(patient.getResistPop(patient.getPrescriptions()))


    return output_tot, output_res
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment(t):

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # make viruses
    maxBirthProb = 0.1
    clearProb = 0.05
    resistances = {'guttagonol': False,
                   'grimpex': False}
    mutProb = 0.005

    viruses = []
    for i in range(0, 100):
        viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

    maxPop = 1000
    patient = Patient(viruses, maxPop)

    output_tot = []
    output_res = []

    # run the first 150 steps
    for j in range(0, 150):
        output_tot.append(patient.update())
        output_res.append(patient.getResistPop(['guttagonol','grimpex']))

    # add the drug then run again for t steps
    patient.addPrescription('guttagonol')
    for j in range(0, t):
        output_tot.append(patient.update())
        output_res.append(patient.getResistPop(patient.getPrescriptions()))

    # add 2nd drug then run again for 150 steps
    patient.addPrescription('grimpex')
    for k in range(0, 150):
        output_tot.append(patient.update())
        output_res.append(patient.getResistPop(patient.getPrescriptions()))

    return output_tot, output_res
    #

#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO



if __name__ == '__main__':

    # simulationWithoutDrug()
    sel = raw_input("""Run which?\n
    1: simulationWithoutDrug\n
    2: simulationWithDrug\n
    3: simulationDelayedTreatment\n
    4: simulationTwoDrugsDelayedTreatment\n
    5: simulationTwoDrugsVirusPopulations\n
    """)

    if sel == '1':
        num_trials = 500
        v_pops = []
        for n in range(0, num_trials):
            v_pops.append(simulationWithoutDrug())

        avg_v_pops = [sum(pop) / float(len(pop)) for pop in zip(*v_pops)]
        pylab.plot(avg_v_pops)
        pylab.show()

    elif sel == '2':
        num_trials = 500
        v_pops_tot = []
        v_pops_res = []

        for n in range(0, num_trials):
            tmp_pop, tmp_res = simulationWithDrug(150)
            v_pops_tot.append(tmp_pop)
            v_pops_res.append(tmp_res)

        avg_v_pops_tot = [sum(pop) / float(len(pop)) for pop in zip(*v_pops_tot)]
        avg_v_pops_res = [sum(pop) / float(len(pop)) for pop in zip(*v_pops_res)]

        pylab.plot(avg_v_pops_tot,label="Total Population")
        pylab.plot(avg_v_pops_res,label="Resistant Population")
        pylab.legend(loc='best')
        pylab.show()

    elif sel == '3':
        num_trials = 30
        time_before_drug = [0,75,150,300]

        final_pops = []
        final_pops_list = []

        for idx, t in enumerate(time_before_drug):
            print "now running for time: " + str(t)
            v_pops_tot = []
            v_pops_res = []
            for n in range(0, num_trials):
                tmp_pop, tmp_res = simulationDelayedTreatment(t)
                v_pops_tot.append(tmp_pop[-1])
                # v_pops_res.append(tmp_res)

            # avg_v_pops_tot = [sum(pop) / float(len(pop)) for pop in zip(*v_pops_tot)]
            # avg_v_pops_res = [sum(pop) / float(len(pop)) for pop in zip(*v_pops_res)]
            final_pops.append(v_pops_tot)
            # final_pops_list.append(final_pops)
            # pylab.figure(idx)
            # pylab.plot(avg_v_pops_tot,label="Total Population")
            # pylab.plot(avg_v_pops_res,label="Resistant Population")
            # pylab.legend(loc='best')



        for idx, p in enumerate(final_pops):
            pylab.figure(idx)
            pylab.hist(p)

        pylab.show()

    elif sel == '4':
        num_trials = 100
        time_before_drug = [0, 75, 150, 300]

        final_pops = []
        final_pops_list = []

        for idx, t in enumerate(time_before_drug):
            print "now running for time: " + str(t)
            v_pops_tot = []
            v_pops_res = []
            for n in range(0, num_trials):
                tmp_pop, tmp_res = simulationTwoDrugsDelayedTreatment(t)
                v_pops_tot.append(tmp_pop)
                v_pops_res.append(tmp_res)

            # avg_v_pops_tot = [sum(pop) / float(len(pop)) for pop in zip(*v_pops_tot)]
            # avg_v_pops_res = [sum(pop) / float(len(pop)) for pop in zip(*v_pops_res)]
            final_pops.append(v_pops_tot)
            # final_pops_list.append(final_pops)
            # pylab.figure(idx)
            # pylab.plot(avg_v_pops_tot,label="Total Population")
            # pylab.plot(avg_v_pops_res,label="Resistant Population")
            # pylab.legend(loc='best')

        for idx, p in enumerate(final_pops):
            pylab.figure(0)
            pylab.subplot(len(final_pops),1,idx+1)
            pylab.hist(p)

        pylab.show()
