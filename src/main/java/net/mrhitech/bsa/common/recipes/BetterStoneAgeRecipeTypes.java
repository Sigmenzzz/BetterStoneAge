package net.mrhitech.bsa.common.recipes;

import net.dries007.tfc.common.recipes.PotRecipe;
import net.minecraft.resources.ResourceLocation;
import net.mrhitech.bsa.BetterStoneAge;

public class BetterStoneAgeRecipeTypes {
    public static void registerPotRecipeOutputTypes() {
        PotRecipe.register(new ResourceLocation(BetterStoneAge.MOD_ID, "porridge"), PorridgePotRecipe.OUTPUT_TYPE);
    }
}
