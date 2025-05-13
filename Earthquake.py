import streamlit as st 
import pandas as pd 
st.set_page_config(page_title="Design Base Shear and Storey Shear for n Storey Building")
st.title("Earthquake Analysis- Design Base Shear and Storey Shear for n Storey Building (Moment Resisting Frame) anywhere in Bangladesh BNBC-2020")

#Load CSV File of Seismic Factor 
st.markdown ("### Select your area and zone value")
st.title("Seismic Zone Value (Z)")
seismic_zone = pd.read_csv("seismic_zone_value.csv")
st.dataframe(seismic_zone)
city= st.text_input ("Write the name of your city :","").strip().title()
seismic_zone_coefficient= st.number_input ("Enter the value of seismic zone coefficient (Z) from the table: ",min_value=0.1,max_value=0.5) 
st.write (f"The location of your structure is **{city}** and The value of Z is **{seismic_zone_coefficient}**")

#Understand Occupancy Factor
st.markdown ("### Find out your occupancy category from the table below")
occupancy_factor_table= pd.read_csv("occupancy_factor_table.csv")
st.dataframe(occupancy_factor_table)
occupancy_category= st.radio(
    "Enter Occupancy Category: ",
    ("I","II","III","IV")
)

#taking value of Occupancy factor

st.markdown ("### Select the value of importance factor from the table below")
occupancy_table= pd.read_csv("occupancy_factor.csv")
st.dataframe(occupancy_table)
importance_factor= st.radio(
    "Value of Importance Factor is:",
    (1.0,1.25,1.50)
)
st.write(f"Occupancy Category is **{occupancy_category}** and importance factor **{importance_factor}**")

#Site classification based on soll type 
st.markdown ("### Select the soil type. You will get the type from your Soil Report")
soil_type= pd.read_csv("soil_classification.csv")
st.dataframe(soil_type)
soil_category= st.radio(
    "Enter soil type: ",
    ("SA","SB","SC","SD","SE")
)
st.write(f"The type of the soil is **{soil_category}**")
st.markdown ("### Now write down the corresponding values of the type of soil")
S= st.number_input ("The value of S is: ")
TB= st.number_input ("The value of TB is: ")
TC= st.number_input ("The value of TC is: ")
TD= st.number_input ("The value of TD is: ")
st.write (f"For soil type **{soil_category}**, S= **{S}**, TB= **{TB}** sec, TC= **{TC}** sec and TD= **{TD}** sec")

#Select zone 
st.markdown ("### Select zone type from the location of your structure")
zone= pd.read_csv("Zones.csv")
st.dataframe(zone)
zone_type= st.radio(
    "Enter Zone type: ",
    (1,2,3,4)
)
st.write(f"The Zone type is **{zone_type}**")

#Building category 
st.markdown ("### Select building category from the soil type")
if occupancy_category== "I"or"II" or "III":
    building01= pd.read_csv ("building01.csv")
    st.dataframe(building01)
    building_category= st.radio(
    "Enter building category: ",
    ("A","B","C","D")
)
    st.write(f"The building category is **{building_category}**")
elif occupancy_category== "IV":
    building02= pd.read_csv ("building02.csv")
    st.dataframe(building02)
    building_category= st.radio(
    "Enter building category: ",
    ("C","D")
)
    st.write(f"The building category is **{building_category}**")
else: 
    st.write ("Please select occupancy category first")

#Take input of load
st.markdown ("### Calculation of Live load and Dead Load")
dead_load= st.number_input ("Enter amount of Dead Load in KN: ",min_value=0.0,max_value=10000000.0)
st.write (f"Total Dead Load is : **{dead_load}** KN")
live_load_floor= st.number_input ("Enter amount of Live Load for floors (kN/m²): ",min_value=0.0,max_value=1000.0)
st.write (f"Floor Live Load is : **{live_load_floor}** (kN/m²)")
live_load_roof= st.number_input ("Enter amount of Live Load for roof (kN/m²): ",min_value=0.0,max_value=1000.0)
st.write (f"Roof Live Load is : **{live_load_roof}** (kN/m²)")
no_storey= st.number_input ("Number of Storey is: ",min_value=1.0,max_value=100.0)
no_roof= 1
plinth_area= st.number_input ("Plinth area is: ",min_value=0.0,max_value=100000.0)
total_live_load= (live_load_floor*(no_storey-1)*plinth_area)+ (no_roof*live_load_roof*plinth_area)
st.write (f"Total Live Load is : **{total_live_load}** kN")
percentage_LL= st.number_input ("What should be the percentage of Live Load: ",min_value=25.0,max_value=100.0)
st.write (f"Percentage of total Live Load to be considered : **{percentage_LL}**%")
total_load= dead_load + (percentage_LL/100)*total_live_load
st.write (f"Total Load (W) : **{total_load}** KN")

#Structure type
st.markdown ("### Select the type of your structure")
type_structure= pd.read_csv ("structure_type.csv")
st.dataframe(type_structure)
structure_type= st.radio(
    "What is the structure type: ",
    ("Concrete moment-resisting frames","Steel moment-resisting frames","Eccentrically braced steel frame","All other structural frames")
) 
ct= st.number_input ("Write down the value of Ct",min_value=0.00000,max_value=1.00000,format="%.4f")
m= st.number_input ("Write down the value of m",min_value=0.00000,max_value=1.00000, format="%.4f")
st.write (f"The structure type is **{structure_type}** and value of ct and m are **{ct}** and **{m}** respectively")

#Calculate Time period 
st.markdown ("### Calculation of Time period")
h= st.number_input ("Total height of the building (meter) is :")
st.write (f"Height of the building is **{h}** meters")
T= ct* (h**m)
st.write (f"Time period is **{T}** s")

#Viscous damping 
st.markdown ("### Calculation of acceleration response spectrum")
d= st.number_input ("What is the percentage of viscous dampinng: ",max_value=28, min_value=1) #Value of damping coefficient must be >0.55 and so max is 28 here
damping_coefficient= (10 / (5 + d))**0.5

#Normalize acceleration response spectrum 
if 0< T <=TB:
    Cs= S* (1+(T/TB)*(2.5*damping_coefficient-1))
    st.write (f"The value of Cs is: **{Cs}**")
elif TB<=T<=TC:
    Cs= 2.5*S*damping_coefficient 
    st.write (f"The value of Cs is: **{Cs}**")
elif TC<=T<=TD: 
    Cs= 2.5*S*damping_coefficient*(TC/T)
    st.write (f"The value of Cs is: **{Cs}**")
elif TD<=T<=4: 
    Cs= 2.5*S*damping_coefficient*((TC*TD)/T**2)
    st.write (f"The value of Cs is: **{Cs}**")   
else: 
    st.write("Missing Values")

st.write (f"The value of acceleration response spectrum, Cs {Cs}")

# Response Factor 
st.markdown ("### Calculation of response factor")
resisting_system= st.selectbox(
    "What is your seismic Force resisting system:",
    ["C: MOMENT RESISTING FRAME SYSTEMS (no shear wall)"]
) 
if resisting_system== "C: MOMENT RESISTING FRAME SYSTEMS (no shear wall)":
    resisting_frame= pd.read_csv("C_type.csv")
    st.dataframe (resisting_frame)
    RF= st.number_input ("Enter the value of response reduction factor,R: ")
    st.write (f"value of response reduction factor,R is **{RF}**")
else: 
    st.write ("Select resisting frame type")

#design spectral acceleration
st.markdown ("### Calculation of spectral acceleration")
Sa= (2/3)*((seismic_zone_coefficient*importance_factor)/RF)*Cs
min_Sa= 0.67* 0.15* seismic_zone_coefficient*importance_factor* S
st.write(f"Value of design spectral acceleration(Sa): {Sa}")
st.write(f"Value of 0.67𝛽ZIS : {min_Sa}")
st.write ("The value of design spectral acceleration(Sa) must be greater than or equal 0.67𝛽ZIS.So if Sa <0.67𝛽ZIS, the value of Sa= 0.67𝛽ZIS")
final_Sa= max (Sa, min_Sa)
st.write(f"Design Spectral Acceleration(Sa): **{final_Sa}**")

#design base shear
st.markdown ("### Calculation of base shear")
st.markdown ("The design base shear,V = Sa*W")
V= final_Sa* total_load
st.write (f"The design base shear is **{V}** KN")

#Final Calculation
st.markdown ("### Calculation of Storey shear")
st.write(r"Approximate weight per floor: $$\left( \frac{\text{Dead Load}}{\text{No. of Storeys}} \right) + (\text{Plinth Area} \times \text{Live Load} \times \text{Live Load Factor})$$")
w_floor= (dead_load/no_storey)+ plinth_area* live_load_floor*(percentage_LL/100)
st.write(f"Approx. weight of the building per Floor is **{w_floor}** KN")
st.write(r"Approximate weight at roof: $$\left( \frac{\text{Dead Load}}{\text{No. of Storeys}} \right) + (\text{Plinth Area} \times \text{Roof Live Load} \times \text{Live Load Factor})$$")
w_roof= (dead_load/no_storey)+ plinth_area* live_load_roof*(percentage_LL/100)
st.write(f"Approx. weight of the building at roof is **{w_roof}** KN")
st.write("For moment resisting frame, stiffness (K) =1")
st.write(r"$$F_n = \frac{V \cdot w_n \cdot h_n^k}{\sum w_n \cdot h^k}$$")
#sum of w and h
h_unit = h / no_storey
cumulative_height = 0.0
total_expression_wh = 0.0

for i in range(1, int(no_storey) + 1):
    cumulative_height += h_unit
    
    # Use w_floor for steps 1 to (n-1), w_roof at step n
    if i < no_storey:
        w_current = w_floor
    else:
        w_current = w_roof

    term = w_current * cumulative_height
    total_expression_wh += term

    st.write(f"Step {i}: Height = {cumulative_height:.2f} m → Term(w*h) = {w_current:.2f}*{cumulative_height:.2f} = {term:.2f} kN·m")

st.write(f"Total Sum of w·h is **{total_expression_wh:.2f} kN·m**")

#Calculation of F
h_unit = h / no_storey
cumulative_height = 0.0
total_expression_F = 0.0
for i in range(1, int(no_storey) + 1):
    cumulative_height += h_unit
    
    # Use w_floor for steps 1 to (n-1), w_roof at step n
    if i < no_storey:
        w_current = w_floor
    else:
        w_current = w_roof

    term = (w_current * cumulative_height * V)/total_expression_wh
    total_expression_F += term

    st.write(f"**F{i} = {term:.2f} kN**")




