# Information Technology Security Methods

## Introduction and Concepts

### Life spheres affected by information security
* Finance and commerce;
* Government;
* Military;
* Private life;

### CIA Triad
* Confidentiality
  * Prevention of unauthorized access
* Integrity
  * Ensuring the accuracy and consistency of data during its life-cycle
* Availability
  * Ensuing access to the data when it is required

### Additional information security tasks
* Authentication
  * Confirmation of the truthfullness of an attribute of an entity
* Nonrepudiation
  * Prevent a sender to take back a message
* Access control
  * Selective restriction of access for a resource

### Infomration Technology differences from reality

|Type|Reality|IT|
|---|---|---|
|***Tampering detection***|Easy|Difficult|
|***Copies***|Difficult|Easy|
|***Signature***|Same for all documents|Different for unique document and signer|

### Asset management

To keep information safe, we need to knw what types of assets we have.

#### Asset Types
* Information
* Electronic documents
* Paper documents
* Software and its code
* Human resources
* Hardware equipment
* Communication lines
* Supporting equipment
* Service
* Relations
* Image

### Vulnerability | Threat | Risk

Vulnerability - something that could be exploited
Threat - the probabilty of exploit
Risk - impact if vulnerability is exploited

### Existing attack types (data in transit)

#### Interruption
![Interruption](img/interruption.png)

#### Interception
![Interception](img/interception.png)

#### Modification
![Modification](img/modification.png)

#### Fabrication
![Fabrication](img/fabrication.png)

### Passive vs Active attacks

* Passive Attack
  * Does not change the flow of information
  * Difficult to detect
* Active Attack
  * Information flow is modified
  * Relatively easy to notice


## Access Control

### Access Control
A set of policies together with a software and/or hardware component, that provide access to a specified resource based on access rights.

### AAA in Access Control
`Authentication`, `Authorization`, `Audit`

### Zero Trust principles
* Single strong source of user identity
* User authentication
* Machine authentication
* Additional context
* Authorization policies
* Access control policies within an application

### Authentication

* Identifification
* Authentication

### Why authentication is required?

Authentication is required for both communication parties to know they communicate with a true entity.

Without authentication, you cannot trust in the correctess of the information received.

### Authentication methods

* What you know?
* What you have?
* What you are?
* Where you are?

### Strong authentication methods
* Multi-factor authentication
* Mutual/two-way authentication
* Strong authentication

### Password Usage Requirements

Requirements are based on the password policy that is in place. 

Possible requirements for a password could be as follows:
* Not a dictionary word
* Not related to public information available about the user
* Not shorter that 8 symbols
* Longer than 15 symbols are recommended
* Use of numbers
* Use of special symbols
* Should be changed regularly, without repeating

### Authorizatin

A process that defines the rights that can be given to an entity that was identified and authenticated.

### Access control models

* Entity types
  * Subjects (giving rights)
  * Objects (being manipulated)

Subjects and objects might be have a different type, based on the context.

#### MAC

Mandatory access control - access rights are granted by the system.

Used in systems that stores information by security levels (public, secret, top secret).

All subjects and objects are assigned with labels. The label shows the trust of assigned subject.

##### Bell-LaPadula Model (BLP)
Uses labels for objects and clearances for subjects.

Focused on *data confidentiality*.

Characterized by the phrase ***write up, read down***.

A subject at a given security level may not read an object with a higher security level (read down)

A subject at given a security level may not write to an object with a lower security level (write up)

##### Biba Model
Uses labels for objects and clearances for subjects.

Focused on *data integrity*.

Inverse of BLP model.

Characterized by the phrase ***write down, read up***.

A subject at a given security level may not read an object with a lower security level (read up)

A subject at given a security level may not write to an object with a higher security level (write down)

### DAC
Discretionary access control - a model where access rights are granted by the owner of an object.

Rules:
* Object has an owner
* Owner can delegate their rights to another
* Access rights are granted by the owner

Uses access control lists (ACL), on file level (read, write, execute) and network level (IPs and ports).

### RBAC

Role-based access control - a model where access rights are given to specific user roles.

* A subject can have multiple roles;
* A role can have multiple subjects;
* A role can have many permissions;
* A permission can be assigned to many roles;
* An operation can be assigned to many permissions;
* A permission can be assigned to many operations;

### Access Matrix Models

> ❗ Needs expansion

### Clarck-Wilson integrity model
Works by use of subject-transaction-object triplet. With this relationship, subject has no direct access to objects.

Focused on integrity.

Required that certifier of transaction and implementer of transaction be different entities.

### ABAC
Attribute-based access control - access is granted based on the attributes that a subject has (e.g. older than 18).

### Break-Glass Access Control Model
Access is given by violation of the regular access model in critical conditions (health/life threat).

### Auditing
Auditing is a process of monitoring and logging of event, errors, connections, authentication attempts.

Audit information should be expansive, to be capable of tracking user activity.

Audit information could be used for detection of security incidents, restoring malicious activity, computer forensics

## Malware

### Key features
* Created with the aim of ***harm***
* Installed ***without*** the knowledge of the user.

### Malware categories

* Infective
* Remote control
* Spyting
* Adware
* Other

> ❗ Needs expansion (Other)

> ⚠️ Skipping:
> * Theory Evolution
> * Unformal Definition
> * Malware Evolution – 1
> * Malware Evolution – 2
> * Malware Evolution – 3

### Malware Marking Scheme

Computer Antivirus Researchers Organisation

```
[<malware_type>://]
[<platform>/]
<family_name>
[<group_name>]
[.<infective_length>]
[.<variant>[<devolution>]]
[<modifiers>]
```

#### `<malware_type>://` 
`Virus://`, `Trojan://`, `Garbage://`, etc.

#### `<platform>/`
`Boot`, `DOS`, `Java`, `Win95`, `ExcelFormula` etc.

### Malware infection strategies

#### Boot sector infection
* Master boot record (MBR)
* DOS boot record (DBR)

#### File infection
* Changing file
* Appending file
* Filling free space
* Compressing file

#### Malware behavior
* Direct action
* Memory resident
* Temporary memory resident
* Swapping
* User mode/Kernel mode
* Propagating via network

### Malware code evolution

* Unencrypted code
* Encrypted code
* Gligomorphic
* Polymorphic
* Metamorphic
* Malware Kits

### Classification (Impact)

* No-payload
* Accidentally destructive payload
* Nondestructive payload
* Destructive payload
* Highly destructive payload
* Destructive for remote systems

### Malware types
* Virus
* Worm
* Mailer/Mass-mailer
* Octopus
* Rabbit
* Trojan Horse
* Logical Bomb
* Easter Egg
* Spyware
* Adware
* Dialer
* Keylogger
* Exploit
* Botnet
* Ransomware
* ATP
* Germs
* Droppers

## Antivirus, IDS/IPS, FIM, Honeypot

### Definition of virus detection
* False-positive - Virus is present, but undetected;
* False-negative - Virus is not present, but detected;
* True-positive - Virus is present and detected;
* True-negative - Virus is not present and not detected.

### What is an antivirus?
A scanner, inspector, monitor, vaccinator.

### Possible protective actions
* Delete the infected file
* Block acess to the infected file
* Quarantine
* Treating

### Malware detection methods
* Signature
* Heuristics
* Anomaly detection
* Sandbox
* Whitelist

#### Signature method
Malware contains unique lines of source code
False-positive rate - low
Signatures are mainly created by hand

* Advantages:
  * Precies
  * Reliable
  * Widely used
* Disadvantages
  * Cannot detect new or polymorphic malware
  * Signature updates can be late
  * Size increase of signature databases

#### Heuristic method
Used when signature does not match 100%.

Applicable for gligomorphic, polymorphic, and metamorphic malware detection

False-positive rate - high

#### Anomaly detection
Monitoring of defined parameters, establishment of threshold criteria

* Advantages:
  * Can detect new malware
  * Dynamic and adaptive
* Disadvantages:
  * Unreliable
  * High false-positive rate
  * Training should be done in a *sterile* environment

#### Sandbox
A protected virtual machine, where malware can be run without harming the host operating system.

* Advantages:
  * Effective
  * Suitable for professional and research usage
  * Effective against gligomorphic, polymorphic, and metamorphic malware
* Disadvantages:
  * Large time consumption
  * Large resource consumption

#### Whitelist

Only whitelisted programs can be executed

* Advantages:
  * No need for signature updates
  * Suitable for large organisations with typical workstations
* Disadvantages:
  * Non-flexible
  * Requires a lot of administration

### Intrusion Detection / Prevention

#### IDS / IPS components

* Sensors/Agents
* Management server
* Database
* Management console
* Secure management network

#### Types

* Rule-based (similar to signature method in malware detection)
* NIDS - network based
* HIDS/FIM - host based
* Honeypot - a bait server