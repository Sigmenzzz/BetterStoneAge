package net.mrhitech.bsa.event;

import net.dries007.tfc.common.blockentities.AbstractFirepitBlockEntity;
import net.dries007.tfc.common.blockentities.TFCBlockEntities;
import net.dries007.tfc.common.blocks.devices.PotBlock;
import net.dries007.tfc.util.events.StartFireEvent;
import net.minecraft.core.BlockPos;
import net.minecraft.world.item.DyeColor;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.event.lifecycle.FMLCommonSetupEvent;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;
import net.mrhitech.bsa.common.blocks.BetterStoneAgeBlocks;
import net.mrhitech.bsa.mixin.BlockEntityTypeAccessor;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.stream.Stream;

public class ForgeEventHandler {
    public static void init() {
        final IEventBus bus = MinecraftForge.EVENT_BUS;
        
        bus.addListener(ForgeEventHandler::onFireStart);
    }
    
    
    public static void onFireStart(StartFireEvent event) {
        Level level = event.getLevel();
        BlockPos pos = event.getPos();
        BlockState state = event.getState();
        Block block = state.getBlock();
        
        
        if (block instanceof PotBlock) {
            final BlockEntity blockEntity = level.getBlockEntity(pos);
            if (blockEntity instanceof AbstractFirepitBlockEntity<?> firepit && firepit.light(state))
            {
                event.setCanceled(true);
            }
        }
    }
    
    // public static void onFireStop(DouseFireEvent event) {
    //     final Level level = event.getLevel();
    //     final BlockPos pos = event.getPos();
    //     final BlockState state = event.getState();
    //     final Block block = state.getBlock();
    //     final Player player = event.getPlayer();
    //    
    //    
    // }
    
    
    
        
}
