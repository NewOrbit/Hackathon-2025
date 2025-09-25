import { createContext, useContext } from "react";

export type MealLogResult = {
  success: boolean;
  message?: string;
  parseError?: boolean;
};

export type MealLogContextValue = {
  logMealFromText: (description: string) => Promise<MealLogResult>;
  canLogMeal: boolean;
};

const MealLogContext = createContext<MealLogContextValue>({
  logMealFromText: async () => ({
    success: false,
    message: "Meal logging is not available right now.",
  }),
  canLogMeal: false,
});

export function useMealLog(): MealLogContextValue {
  return useContext(MealLogContext);
}

export default MealLogContext;
