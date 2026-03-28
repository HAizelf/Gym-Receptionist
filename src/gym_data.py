"""Gym data for Hype The Gym, Sector 93."""

GYM_TIMINGS = {
    "Monday": "6:00 AM - 10:00 PM",
    "Tuesday": "6:00 AM - 10:00 PM",
    "Wednesday": "6:00 AM - 10:00 PM",
    "Thursday": "6:00 AM - 10:00 PM",
    "Friday": "6:00 AM - 10:00 PM",
    "Saturday": "7:00 AM - 9:00 PM",
    "Sunday": "7:00 AM - 9:00 PM",
}

MEMBERSHIP_PLANS = [
    {
        "name": "Monthly",
        "duration": "1 month",
        "price": "2,500 rupees",
        "includes": "Full gym access, locker room",
    },
    {
        "name": "Quarterly",
        "duration": "3 months",
        "price": "6,000 rupees",
        "includes": "Full gym access, locker room, one free personal training session",
    },
    {
        "name": "Half-Yearly",
        "duration": "6 months",
        "price": "10,000 rupees",
        "includes": "Full gym access, locker room, three free personal training sessions",
    },
    {
        "name": "Annual",
        "duration": "12 months",
        "price": "18,000 rupees",
        "includes": "Full gym access, locker room, six free personal training sessions, diet consultation",
    },
]

TRAINERS = [
    {
        "name": "Rahul Sharma",
        "specialty": "Strength and conditioning",
        "experience": "8 years",
        "availability": "Monday to Saturday, 7 AM to 3 PM",
    },
    {
        "name": "Priya Verma",
        "specialty": "Weight loss and functional training",
        "experience": "5 years",
        "availability": "Monday to Friday, 4 PM to 9 PM",
    },
    {
        "name": "Amit Chauhan",
        "specialty": "Bodybuilding and powerlifting",
        "experience": "10 years",
        "availability": "Monday to Saturday, 6 AM to 12 PM",
    },
]

EQUIPMENT = {
    "Cardio": [
        "Treadmills",
        "Elliptical trainers",
        "Stationary bikes",
        "Rowing machines",
        "Stair climbers",
    ],
    "Strength": [
        "Flat and incline benches",
        "Squat racks",
        "Smith machine",
        "Leg press",
        "Cable crossover machine",
        "Lat pulldown machine",
    ],
    "Free Weights": [
        "Dumbbells from 2.5 to 50 kilograms",
        "Barbells and Olympic bars",
        "Kettlebells",
        "Weight plates",
    ],
    "Functional Training": [
        "Battle ropes",
        "TRX suspension trainers",
        "Resistance bands",
        "Medicine balls",
        "Plyo boxes",
    ],
}
