"use client";

import { motion, type MotionProps } from "motion/react";
import type React from "react";

interface AnimatedElementProps extends MotionProps {
  children: React.ReactNode;
  delay?: number;
}

export const AnimatedElement: React.FC<AnimatedElementProps> = ({
  children,
  delay = 0,
  ...props
}) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      {...props}
    >
      {children}
    </motion.div>
  );
};
