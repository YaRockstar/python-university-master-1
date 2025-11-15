"""Паттерны проектирования для транспортной компании."""
from application.patterns.chain_of_responsibility import Handler, Mechanic, DepartmentHead, Director, MaintenanceRequest
from application.patterns.template_method import CostCalculator, BusCostCalculator, TruckCostCalculator

__all__ = [
    "Handler",
    "Mechanic",
    "DepartmentHead",
    "Director",
    "MaintenanceRequest",
    "CostCalculator",
    "BusCostCalculator",
    "TruckCostCalculator",
]

