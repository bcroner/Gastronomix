"""
Gastronomix: A Computational Culinary Arts Framework
A foundational boilerplate for building custom data-driven kitchen software.
"""

from typing import Dict, List, Optional


class Ingredient:
    """Represents a culinary ingredient with physical and nutritional properties."""
    
    def __init__(
        self, 
        name: str, 
        density_g_ml: float = 1.0, 
        water_content_pct: float = 0.0,
        attributes: Optional[Dict[str, any]] = None
    ):
        self.name = name
        self.density_g_ml = density_g_ml  # Useful for volume-to-weight conversions
        self.water_content_pct = water_content_pct
        self.attributes = attributes or {}

    def __repr__(self) -> str:
        return f"Ingredient({self.name})"


class RecipeComponent:
    """Links an ingredient to a specific mass in a recipe."""
    
    def __init__(self, ingredient: Ingredient, mass_g: float):
        self.ingredient = ingredient
        self.mass_g = mass_g

    @property
    def volume_ml(self) -> float:
        """Calculates volume based on ingredient density."""
        return self.mass_g / self.ingredient.density_g_ml


class CulinaryFormula:
    """
    Models a recipe as a computational formula.
    Supports scaling, hydration analysis, and baker's percentage calculations.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.components: Dict[str, RecipeComponent] = {}
        self.steps: List[str] = []

    def add_ingredient(self, ingredient: Ingredient, mass_g: float):
        """Adds or updates an ingredient mass in the formula."""
        self.components[ingredient.name] = RecipeComponent(ingredient, mass_g)

    def add_step(self, instruction: str):
        """Appends a procedural step to the execution timeline."""
        self.steps.append(instruction)

    @property
    def total_mass(self) -> float:
        """Returns total mass of all components combined."""
        return sum(comp.mass_g for comp in self.components.values())

    def get_bakers_percentages(self, primary_ingredient_name: str) -> Dict[str, float]:
        """
        Calculates the ratio of each ingredient relative to a primary base (e.g., Flour).
        In computational baking, the primary ingredient is always 100%.
        """
        if primary_ingredient_name not in self.components:
            raise ValueError(f"{primary_ingredient_name} not found in formula.")
            
        base_mass = self.components[primary_ingredient_name].mass_g
        return {
            name: (comp.mass_g / base_mass) * 100 
            for name, comp in self.components.items()
        }

    def scale_by_total_mass(self, target_mass_g: float) -> 'CulinaryFormula':
        """Returns a new scaled instance of the formula to meet a target yield."""
        current_total = self.total_mass
        if current_total == 0:
            raise ValueError("Cannot scale an empty formula.")
            
        scaling_factor = target_mass_g / current_total
        
        scaled_formula = CulinaryFormula(f"{self.name} (Scaled)")
        for comp in self.components.values():
            scaled_formula.add_ingredient(comp.ingredient, comp.mass_g * scaling_factor)
        
        scaled_formula.steps = self.steps.copy()
        return scaled_formula


# ==========================================
# SIMULATION / EXAMPLE USAGE
# ==========================================
if __name__ == "__main__":
    print("--- Initializing Gastronomix Computational Engine ---")
    
    # 1. Define modular ingredients with physical profiles
    flour = Ingredient("Bread Flour", density_g_ml=0.57, water_content_pct=14.0)
    water = Ingredient("Distilled Water", density_g_ml=1.0, water_content_pct=100.0)
    salt = Ingredient("Fine Sea Salt", density_g_ml=1.2, water_content_pct=0.0)
    yeast = Ingredient("Instant Yeast", density_g_ml=0.42, water_content_pct=0.0)
    
    # 2. Build a baseline sourdough / bread formula
    bread_formula = CulinaryFormula("Sourdough Base")
    bread_formula.add_ingredient(flour, 500.0)
    bread_formula.add_ingredient(water, 350.0)  # 70% Hydration
    bread_formula.add_ingredient(salt, 10.0)     # 2% Salt
    bread_formula.add_ingredient(yeast, 5.0)     # 1% Yeast
    
    bread_formula.add_step("Autolyse flour and water for 45 minutes.")
    bread_formula.add_step("Incorporate yeast and salt; knead until windowpane stage.")
    
    # 3. Analyze baseline analytics
    print(f"\nFormula Name: {bread_formula.name}")
    print(f"Total Batch Weight: {bread_formula.total_mass}g")
    
    print("\n[Baker's Percentages]")
    percentages = bread_formula.get_bakers_percentages("Bread Flour")
    for ing_name, pct in percentages.items():
        print(f"  {ing_name}: {pct:.1f}%")
        
    # 4. Compute algorithm-driven scaling
    # Let's say a restaurant needs exactly a 1200g batch size
    target_weight = 1200.0
    scaled_bread = bread_formula.scale_by_total_mass(target_weight)
    
    print(f"\n[Scaled Yield Matrix - Target: {target_weight}g]")
    for name, comp in scaled_bread.components.items():
        print(f"  {name}: {comp.mass_g:.1f}g (~{comp.volume_ml:.1f} mL)")
        
    print("\n[Execution Blueprint]")
    for idx, step in enumerate(scaled_bread.steps, 1):
        print(f"  {idx}. {step}")
