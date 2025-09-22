<template>
  <div class="min-h-screen bg-neutral-50 py-10">
    <div class="container-custom">
      <div class="max-w-7xl mx-auto">
        <!-- Cabecera -->
        <div class="text-center mb-10">
          <h1 class="text-3xl font-display font-bold text-neutral-900 mb-3">Completa tu perfil</h1>
          <p class="text-neutral-600">Elige un plan y configura tu perfil profesional</p>
        </div>
        
        <!-- Pasos -->
        <div class="flex justify-between items-center mb-8">
          <div class="flex-1 flex flex-col items-center">
            <div class="w-10 h-10 rounded-full bg-primary-600 text-white flex items-center justify-center font-medium">1</div>
            <span class="text-sm mt-2 text-primary-600 font-medium">Tipo</span>
          </div>
          <div class="flex-1 h-1 bg-neutral-200">
            <div class="h-full bg-primary-600" :style="`width: ${currentStep > 1 ? '100%' : '0%'}`"></div>
          </div>
          <div class="flex-1 flex flex-col items-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-medium"
                 :class="currentStep >= 2 ? 'bg-primary-600 text-white' : 'bg-neutral-200 text-neutral-500'">2</div>
            <span class="text-sm mt-2" :class="currentStep >= 2 ? 'text-primary-600 font-medium' : 'text-neutral-500'">{{ userType === 'prestador' ? 'Plan' : 'Perfil' }}</span>
          </div>
          <div v-if="userType === 'prestador'" class="flex-1 h-1 bg-neutral-200">
            <div class="h-full bg-primary-600" :style="`width: ${currentStep > 2 ? '100%' : '0%'}`"></div>
          </div>
          <div v-if="userType === 'prestador'" class="flex-1 flex flex-col items-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-medium"
                 :class="currentStep >= 3 ? 'bg-primary-600 text-white' : 'bg-neutral-200 text-neutral-500'">3</div>
            <span class="text-sm mt-2" :class="currentStep >= 3 ? 'text-primary-600 font-medium' : 'text-neutral-500'">Perfil</span>
          </div>
          <div v-if="userType === 'prestador'" class="flex-1 h-1 bg-neutral-200">
            <div class="h-full bg-primary-600" :style="`width: ${currentStep > 3 ? '100%' : '0%'}`"></div>
          </div>
          <div v-if="userType === 'prestador'" class="flex-1 flex flex-col items-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-medium"
                 :class="currentStep >= 4 ? 'bg-primary-600 text-white' : 'bg-neutral-200 text-neutral-500'">4</div>
            <span class="text-sm mt-2" :class="currentStep >= 4 ? 'text-primary-600 font-medium' : 'text-neutral-500'">Servicios</span>
          </div>
          <div v-if="userType === 'prestador'" class="flex-1 h-1 bg-neutral-200">
            <div class="h-full bg-primary-600" :style="`width: ${currentStep > 4 ? '100%' : '0%'}`"></div>
          </div>
          <div v-if="userType === 'prestador'" class="flex-1 flex flex-col items-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-medium"
                 :class="currentStep >= 5 ? 'bg-primary-600 text-white' : 'bg-neutral-200 text-neutral-500'">5</div>
            <span class="text-sm mt-2" :class="currentStep >= 5 ? 'text-primary-600 font-medium' : 'text-neutral-500'">Resumen</span>
          </div>
        </div>
        
        <!-- Contenido principal -->
        <div class="bg-white rounded-2xl shadow-lg border border-neutral-100 p-6 md:p-8">
          <!-- Paso 1: Selección de tipo de usuario -->
          <div v-if="currentStep === 1" class="space-y-6">
            <h2 class="text-xl font-semibold text-neutral-900 mb-4">¿Cómo quieres usar De Confianza?</h2>
            
            <div class="space-y-4">
              <div 
                class="border rounded-lg p-6 cursor-pointer transition-all"
                :class="userType === 'cliente' ? 'border-primary-500 bg-primary-50 shadow-sm' : 'border-neutral-200 hover:border-primary-300'"
                @click="userType = 'cliente'"
              >
                <div class="flex items-start">
                  <div class="flex items-center h-5 mt-1">
                    <input 
                      type="radio" 
                      id="cliente" 
                      value="cliente" 
                      v-model="userType"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded-full"
                    />
                  </div>
                  <div class="ml-3 flex-1">
                    <label for="cliente" class="font-semibold text-neutral-900 text-lg mb-2 block cursor-pointer">
                      <font-awesome-icon :icon="['fas', 'search']" class="mr-2 text-primary-600" />
                      Buscar servicios
                    </label>
                    <p class="text-neutral-600 text-sm">Quiero encontrar profesionales y prestadores de servicios para mis necesidades.</p>
                  </div>
                </div>
              </div>
              
              <div 
                class="border rounded-lg p-6 cursor-pointer transition-all"
                :class="userType === 'prestador' ? 'border-primary-500 bg-primary-50 shadow-sm' : 'border-neutral-200 hover:border-primary-300'"
                @click="userType = 'prestador'"
              >
                <div class="flex items-start">
                  <div class="flex items-center h-5 mt-1">
                    <input 
                      type="radio" 
                      id="prestador" 
                      value="prestador" 
                      v-model="userType"
                      class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-neutral-300 rounded-full"
                    />
                  </div>
                  <div class="ml-3 flex-1">
                    <label for="prestador" class="font-semibold text-neutral-900 text-lg mb-2 block cursor-pointer">
                      <font-awesome-icon :icon="['fas', 'briefcase']" class="mr-2 text-primary-600" />
                      Ofrecer servicios
                    </label>
                    <p class="text-neutral-600 text-sm">Soy un profesional o prestador de servicios y quiero dar a conocer mi trabajo.</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="flex justify-end mt-6">
              <button 
                @click="nextStep" 
                class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                :disabled="!userType"
              >
                Continuar
              </button>
            </div>
          </div>
          
          <!-- Paso 2: Selección de plan (solo para prestadores) o Perfil básico (para clientes) -->
          <div v-else-if="currentStep === 2" class="space-y-6">
            <!-- Para prestadores: selección de plan -->
            <div v-if="userType === 'prestador'">
              <h2 class="text-xl font-semibold text-neutral-900 mb-4">Elige tu plan</h2>
              
              <!-- Estado de carga -->
              <div v-if="loadingPlans" class="text-center py-8">
                <font-awesome-icon :icon="['fas', 'spinner']" class="text-primary-600 text-2xl animate-spin" />
                <p class="text-neutral-600 mt-2">Cargando planes...</p>
              </div>
              
              <!-- Error al cargar -->
              <div v-else-if="loadError" class="text-center py-8">
                <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="text-red-500 text-2xl" />
                <p class="text-red-600 mt-2">{{ loadError }}</p>
                <button @click="$router.go(0)" class="mt-4 text-primary-600 hover:text-primary-700">
                  Intentar de nuevo
                </button>
              </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6 items-stretch">
              <div
                v-for="plan in subscriptionPlans"
                :key="plan.code"
                class="border rounded-xl p-5 cursor-pointer transition-all hover:shadow-md h-full flex flex-col"
                :class="selectedPlan === plan.code ? 'border-primary-500 bg-primary-50 shadow-sm' : 'border-neutral-200'"
                @click="selectedPlan = plan.code"
              >
                <div class="flex items-center justify-between mb-2">
                  <h3 class="text-lg font-semibold text-neutral-900">{{ plan.name }}</h3>
                  <span class="text-primary-700 font-semibold">{{ formatPriceText(plan.priceText) }}</span>
                </div>
                <ul class="mt-3 space-y-2">
                  <li v-for="(benefit, idx) in getPlanBenefits(plan)" :key="idx" class="flex items-start">
                    <span class="text-primary-500 mr-2 mt-0.5">
                      <font-awesome-icon :icon="['fas', 'check']" />
                    </span>
                    <span class="text-sm text-neutral-700">{{ benefit }}</span>
                  </li>
                </ul>
                <!-- Límites de media -->
                <div class="mt-4 text-sm text-neutral-700 grid grid-cols-2 gap-2">
                  <div class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'image']" class="text-primary-500 mr-2" />
                    <span>Imágenes: {{ plan.maxImages }}</span>
                  </div>
                  <div class="flex items-center">
                    <font-awesome-icon :icon="['fas', 'video']" class="text-primary-500 mr-2" />
                    <span>Videos: {{ plan.maxVideos }}</span>
                  </div>
                </div>
                <!-- Campos habilitados -->
                <div v-if="plan.fieldsEnabled && plan.fieldsEnabled.length" class="mt-3">
                  <div class="text-xs text-neutral-500 mb-1">Campos habilitados</div>
                  <div class="flex flex-wrap gap-2">
                    <span 
                      v-for="field in plan.fieldsEnabled" 
                      :key="field"
                      class="text-xs px-2 py-1 rounded-full border border-neutral-300 text-neutral-700 bg-neutral-50"
                    >
                      {{ fieldLabel(field) }}
                    </span>
                  </div>
                </div>
                <div class="mt-4 pt-2 mt-auto">
                  <button
                    type="button"
                    class="w-full border border-primary-600 text-primary-700 hover:bg-primary-600 hover:text-white font-medium py-2 px-4 rounded-lg transition-colors"
                    :class="selectedPlan === plan.code ? 'bg-primary-600 text-white' : ''"
                    @click.stop="selectedPlan = plan.code"
                  >
                    Elegir {{ plan.name }}
                  </button>
                </div>
              </div>
            </div>
            
              <div class="flex justify-between mt-6">
                <button 
                  type="button"
                  @click="prevStep" 
                  class="border border-neutral-300 hover:bg-neutral-50 text-neutral-700 font-medium py-2 px-6 rounded-lg transition-colors"
                >
                  Atrás
                </button>
                <button 
                  @click="nextStep" 
                  class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                  :disabled="!selectedPlan"
                >
                  Continuar
                </button>
              </div>
            </div>
            
            <!-- Para clientes: información básica -->
            <div v-else>
              <h2 class="text-xl font-semibold text-neutral-900 mb-4">Información básica</h2>
              
              <form @submit.prevent="nextStep" class="space-y-5">
                <div class="grid md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                      Teléfono (opcional)
                      <span v-if="!isFieldEnabled('telefono')" class="ml-2 text-xs text-neutral-500">(bloqueado por plan)</span>
                    </label>
                    <input 
                      type="tel" 
                      v-model="profileData.telefono"
                      :disabled="!isFieldEnabled('telefono')"
                      class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                      placeholder="Teléfono de contacto"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                      Ciudad
                      <span v-if="!isFieldEnabled('ciudad')" class="ml-2 text-xs text-neutral-500" title="Disponible en planes superiores">(bloqueado por plan)</span>
                    </label>
                    <input 
                      type="text" 
                      v-model="profileData.ciudad"
                      :disabled="!isFieldEnabled('ciudad')"
                      class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                      placeholder="Tu ciudad"
                    />
                  </div>
                </div>
                
                <div class="flex justify-between mt-6">
                  <button 
                    type="button"
                    @click="prevStep" 
                    class="border border-neutral-300 hover:bg-neutral-50 text-neutral-700 font-medium py-2 px-6 rounded-lg transition-colors"
                  >
                    Atrás
                  </button>
                  <button 
                    type="button"
                    @click="finishOnboarding" 
                    class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                  >
                    Finalizar
                  </button>
                </div>
              </form>
            </div>
          </div>
          
          <!-- Paso 3: Información de perfil (para prestadores) -->
          <div v-else-if="currentStep === 3 && userType === 'prestador'" class="space-y-6">
            <h2 class="text-xl font-semibold text-neutral-900 mb-4">Información de perfil</h2>
            
            <form @submit.prevent="nextStep" class="space-y-5">
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                    Teléfono
                    <span v-if="!isFieldEnabled('telefono')" class="ml-2 text-xs text-neutral-500" title="Disponible en planes superiores">(bloqueado por plan)</span>
                  </label>
                  <input 
                    type="tel" 
                    v-model="profileData.telefono"
                    :disabled="!isFieldEnabled('telefono')"
                    class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                    placeholder="Teléfono de contacto"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                    Dirección
                    <span v-if="!isFieldEnabled('direccion')" class="ml-2 text-xs text-neutral-500" title="Disponible en planes superiores">(bloqueado por plan)</span>
                  </label>
                  <input 
                    type="text" 
                    v-model="profileData.direccion"
                    :disabled="!isFieldEnabled('direccion')"
                    class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                    Ciudad
                    <span v-if="!isFieldEnabled('ciudad')" class="ml-2 text-xs text-neutral-500" title="Disponible en planes superiores">(bloqueado por plan)</span>
                  </label>
                  <input 
                    type="text" 
                    v-model="profileData.ciudad"
                    :disabled="!isFieldEnabled('ciudad')"
                    class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                    required
                  />
                </div>
              </div>
              
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                    Provincia
                    <span v-if="!isFieldEnabled('provincia')" class="ml-2 text-xs text-neutral-500" title="Disponible en planes superiores">(bloqueado por plan)</span>
                  </label>
                  <input 
                    type="text" 
                    v-model="profileData.provincia"
                    :disabled="!isFieldEnabled('provincia')"
                    class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                    Sitio web
                    <span v-if="!isFieldEnabled('sitio_web')" class="ml-2 text-xs text-neutral-500" title="Disponible en planes superiores">(bloqueado por plan)</span>
                  </label>
                  <input 
                    type="url" 
                    v-model="profileData.sitio_web"
                    :disabled="!isFieldEnabled('sitio_web')"
                    class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                    placeholder="https://ejemplo.com"
                  />
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-1 flex items-center">
                  Descripción
                  <span v-if="!isFieldEnabled('descripcion')" class="ml-2 text-xs text-neutral-500" title="Disponible en planes superiores">(bloqueado por plan)</span>
                </label>
                <textarea 
                  v-model="profileData.descripcion"
                  rows="4"
                  :disabled="!isFieldEnabled('descripcion')"
                  class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors disabled:bg-neutral-100 disabled:text-neutral-500" 
                  required
                ></textarea>
              </div>
              
              <div class="flex justify-between mt-6">
                <button 
                  type="button"
                  @click="prevStep" 
                  class="border border-neutral-300 hover:bg-neutral-50 text-neutral-700 font-medium py-2 px-6 rounded-lg transition-colors"
                >
                  Atrás
                </button>
                <button 
                  type="submit" 
                  class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                >
                  Continuar
                </button>
              </div>
            </form>
          </div>
          
          <!-- Paso 4: Servicios ofrecidos (para prestadores) -->
          <div v-else-if="currentStep === 4 && userType === 'prestador'" class="space-y-6">
            <h2 class="text-xl font-semibold text-neutral-900 mb-4">Servicios que ofreces</h2>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">Categoría</label>
                <select 
                  v-model="selectedCategory"
                  class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors appearance-none" 
                  :class="{'text-neutral-400': !selectedCategory}"
                  required
                >
                  <option value="" disabled>Selecciona una categoría</option>
                  <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-neutral-700 mb-2">Rubro</label>
                <select 
                  v-model="selectedRubro"
                  class="w-full px-3 py-2 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none transition-colors appearance-none" 
                  :class="{'text-neutral-400': !selectedRubro}"
                  required
                  :disabled="!selectedCategory"
                >
                  <option value="" disabled>
                    {{ !selectedCategory ? 'Primero selecciona una categoría' : 'Selecciona un rubro' }}
                  </option>
                  <option v-for="rubro in filteredRubros" :key="rubro.id" :value="rubro.id">
                    {{ rubro.name }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="flex justify-between mt-6">
              <button 
                @click="prevStep" 
                class="border border-neutral-300 hover:bg-neutral-50 text-neutral-700 font-medium py-2 px-6 rounded-lg transition-colors"
              >
                Atrás
              </button>
              <button 
                @click="nextStep" 
                class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
                :disabled="!selectedCategory || !selectedRubro"
              >
                Continuar
              </button>
            </div>
          </div>
          
          <!-- Paso 5: Resumen y pago (para prestadores) -->
          <div v-else-if="currentStep === 5 && userType === 'prestador'" class="space-y-6">
            <h2 class="text-xl font-semibold text-neutral-900 mb-4">Resumen de tu suscripción</h2>
            
            <div class="bg-neutral-50 rounded-lg p-6">
              <div class="grid md:grid-cols-2 gap-6">
                <!-- Plan seleccionado -->
                <div class="bg-white rounded-lg p-4 border border-neutral-200">
                  <h3 class="font-semibold text-neutral-900 mb-2">Plan seleccionado</h3>
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-lg font-medium">{{ selectedPlanData?.name }}</span>
                      <span class="text-xl font-bold text-primary-600">{{ formatPriceText(selectedPlanData?.price_text) }}</span>
                    </div>
                    <p class="text-sm text-neutral-600">{{ selectedPlanData?.description }}</p>
                  </div>
                  
                  <div class="mt-4">
                    <h4 class="font-medium text-neutral-800 mb-2">Beneficios incluidos:</h4>
                    <ul class="space-y-1 text-sm text-neutral-700">
                      <li v-for="benefit in getPlanBenefits(selectedPlanData)" :key="benefit" class="flex items-center">
                        <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 mr-2 text-xs" />
                        {{ benefit }}
                      </li>
                    </ul>
                  </div>
                  
                  <div class="mt-4 pt-4 border-t border-neutral-100">
                    <div class="flex justify-between text-sm text-neutral-600">
                      <span>Imágenes:</span>
                      <span>{{ selectedPlanData?.max_images === 0 ? 'Ilimitadas' : selectedPlanData?.max_images }}</span>
                    </div>
                    <div class="flex justify-between text-sm text-neutral-600">
                      <span>Videos:</span>
                      <span>{{ selectedPlanData?.max_videos === 0 ? 'Ilimitados' : selectedPlanData?.max_videos }}</span>
                    </div>
                  </div>
                </div>
                
                <!-- Información del perfil -->
                <div class="bg-white rounded-lg p-4 border border-neutral-200">
                  <h3 class="font-semibold text-neutral-900 mb-2">Tu información</h3>
                  <div class="space-y-2 text-sm">
                    <div v-if="selectedCategoryName">
                      <span class="font-medium text-neutral-700">Categoría:</span>
                      <span class="ml-2 text-neutral-600">{{ selectedCategoryName }}</span>
                    </div>
                    <div v-if="selectedRubroName">
                      <span class="font-medium text-neutral-700">Rubro:</span>
                      <span class="ml-2 text-neutral-600">{{ selectedRubroName }}</span>
                    </div>
                    <div v-if="profileData.telefono">
                      <span class="font-medium text-neutral-700">Teléfono:</span>
                      <span class="ml-2 text-neutral-600">{{ profileData.telefono }}</span>
                    </div>
                    <div v-if="profileData.ciudad">
                      <span class="font-medium text-neutral-700">Ciudad:</span>
                      <span class="ml-2 text-neutral-600">{{ profileData.ciudad }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div class="flex items-start">
                <font-awesome-icon :icon="['fas', 'info-circle']" class="text-blue-600 mr-3 mt-0.5" />
                <div>
                  <h4 class="font-medium text-blue-900">Próximos pasos</h4>
                  <p class="text-sm text-blue-800 mt-1">
                    <span v-if="isSelectedPlanFree()">
                      Tu plan gratuito se activará inmediatamente. Podrás comenzar a usar la plataforma de inmediato.
                    </span>
                    <span v-else>
                      Serás redirigido a MercadoPago para completar el pago de tu suscripción. 
                      Una vez confirmado el pago, tu plan se activará automáticamente.
                    </span>
                  </p>
                </div>
              </div>
            </div>
            
            <div class="flex justify-between">
              <button 
                @click="prevStep" 
                class="border border-neutral-300 hover:bg-neutral-50 text-neutral-700 font-medium py-2 px-6 rounded-lg transition-colors"
              >
                Atrás
              </button>
              <button 
                @click="procesarPago" 
                :disabled="procesandoPago"
                class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-3 px-8 rounded-lg transition-colors flex items-center"
              >
                <font-awesome-icon v-if="procesandoPago" :icon="['fas', 'spinner']" class="animate-spin mr-2" />
                <font-awesome-icon v-else-if="isSelectedPlanFree()" :icon="['fas', 'check']" class="mr-2" />
                <font-awesome-icon v-else :icon="['fas', 'credit-card']" class="mr-2" />
                <span v-if="procesandoPago">Procesando...</span>
                <span v-else-if="isSelectedPlanFree()">Continuar Gratis</span>
                <span v-else>Suscribirse con MercadoPago</span>
              </button>
            </div>
          </div>
          
          <!-- Paso final: Completado -->
          <div v-else-if="(currentStep === 3 && userType === 'cliente') || (currentStep === 6 && userType === 'prestador')" class="text-center py-6">
            <div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <font-awesome-icon :icon="['fas', 'check']" class="text-green-500 text-3xl" />
            </div>
            <h2 class="text-2xl font-semibold text-neutral-900 mb-2">¡Perfil completado!</h2>
            <p class="text-neutral-600 mb-8">Tu perfil ha sido configurado correctamente.</p>
            <button 
              @click="goToDashboard" 
              class="bg-primary-600 hover:bg-primary-700 text-white font-medium py-2 px-6 rounded-lg transition-colors"
            >
              Ir al panel
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import { onboardingService, catalogService, mercadoPagoService } from '../services/api';

const router = useRouter();
const authStore = useAuthStore();

// Estado del onboarding
const currentStep = ref(1);
const userType = ref(null); // 'cliente' o 'prestador'
const selectedPlan = ref(null);
const selectedCategory = ref(null);
const selectedRubro = ref(null);
const selectedServices = ref([]);
const profileData = ref({
  telefono: '',
  direccion: '',
  ciudad: '',
  provincia: '',
  sitio_web: '',
  descripcion: ''
});

// Planes desde backend
const subscriptionPlans = ref([]);
const loadingPlans = ref(false);
const loadError = ref('');

// Función para convertir campos habilitados en descripciones amigables
const getFieldDescription = (field) => {
  const descriptions = {
    'telefono': 'Mostrar teléfono de contacto',
    'direccion': 'Mostrar dirección del negocio',
    'ciudad': 'Mostrar ciudad de ubicación',
    'provincia': 'Mostrar provincia',
    'sitio_web': 'Incluir enlace a sitio web',
    'descripcion': 'Mostrar descripción del servicio'
  };
  return descriptions[field] || field;
};

// Función para obtener beneficios del plan basado en campos habilitados
const getPlanBenefits = (plan) => {
  if (!plan || !Array.isArray(plan.fieldsEnabled)) return [];
  
  const benefits = plan.fieldsEnabled.map(field => getFieldDescription(field));
  
  // Agregar beneficios adicionales basados en max_images y max_videos
  if (plan.maxImages > 0) {
    benefits.push(`Hasta ${plan.maxImages} imágenes`);
  }
  if (plan.maxVideos > 0) {
    benefits.push(`Hasta ${plan.maxVideos} videos`);
  }
  
  return benefits;
};

// Estado de pago
const procesandoPago = ref(false);

onMounted(async () => {
  try {
    loadingPlans.value = true;
    const { data } = await onboardingService.getPlanes();
    // Adaptar datos del backend (PlanSerializer) al formato de UI
    subscriptionPlans.value = data.map(p => ({
      id: p.id,
      code: p.code,
      name: p.name,
      priceText: p.price_text,
      fieldsEnabled: Array.isArray(p.fields_enabled) ? p.fields_enabled : [],
      maxImages: typeof p.max_images === 'number' ? p.max_images : 0,
      maxVideos: typeof p.max_videos === 'number' ? p.max_videos : 0,
    }));
  } catch (e) {
    console.error('Error cargando planes:', e);
    loadError.value = 'No se pudieron cargar los planes';
  } finally {
    loadingPlans.value = false;
  }
  // Cargar catálogo dinámico
  await loadCatalog();
});

const categories = ref([]);
const rubros = ref([]);

// Rubros filtrados por categoría
const filteredRubros = computed(() => {
  if (!selectedCategory.value) return [];
  return rubros.value.filter(rubro => String(rubro.categoria) === String(selectedCategory.value));
});

// Computed properties para el resumen
const selectedPlanData = computed(() => {
  return subscriptionPlans.value.find(p => p.code === selectedPlan.value) || null;
});

const selectedCategoryName = computed(() => {
  const category = categories.value.find(c => c.id === selectedCategory.value);
  return category ? category.name : '';
});

const selectedRubroName = computed(() => {
  const rubro = rubros.value.find(r => r.id === selectedRubro.value);
  return rubro ? rubro.name : '';
});

async function loadCatalog() {
  try {
    console.log('Cargando catálogo...');
    const [catRes, rubRes] = await Promise.all([
      catalogService.getCategorias(),
      catalogService.getRubros(),
    ]);
    console.log('Respuesta categorías:', catRes.data);
    console.log('Respuesta rubros:', rubRes.data);
    
    // Los endpoints devuelven paginación, usar .results
    const categoriesData = catRes.data.results || catRes.data;
    const rubrosData = rubRes.data.results || rubRes.data;
    
    categories.value = categoriesData.map(c => ({ id: c.id, name: c.nombre }));
    rubros.value = rubrosData.map(r => ({ id: r.id, name: r.nombre, categoria: r.categoria }));
    
    console.log('Categorías procesadas:', categories.value);
    console.log('Rubros procesados:', rubros.value);
  } catch (e) {
    console.error('Error cargando catálogo:', e);
  }
}

// Navegación entre pasos
function nextStep() {
  // Para clientes: máximo 3 pasos (tipo -> perfil -> completado)
  // Para prestadores: máximo 5 pasos (tipo -> plan -> perfil -> servicios -> completado)
  const maxSteps = userType.value === 'cliente' ? 3 : 5;
  if (currentStep.value < maxSteps) {
    // Capturar posición actual del scroll
    const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    currentStep.value++;
    
    // Usar nextTick para asegurar que el DOM se actualice antes de ajustar scroll
    nextTick(() => {
      // Si el usuario estaba en la parte superior, mantenerlo ahí
      // Si no, mantener una posición razonable (parte superior para mejor UX)
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}

function prevStep() {
  if (currentStep.value > 1) {
    // Capturar posición actual del scroll
    const currentScrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    currentStep.value--;
    
    // Usar nextTick para asegurar que el DOM se actualice antes de ajustar scroll
    nextTick(() => {
      // Volver al inicio para mejor UX al retroceder
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}

// Finalizar onboarding
async function finishOnboarding() {
  try {
    // Preparar datos de perfil permitidos por plan
    const perfilPayload = getAllowedPerfilPayload();
    
    // Para prestadores, incluir categoría y rubro
    if (userType.value === 'prestador') {
      if (selectedCategory.value) perfilPayload.categoria = selectedCategory.value;
      if (selectedRubro.value) perfilPayload.rubro = selectedRubro.value;
    }
    
    // Datos completos para onboarding
    const data = {
      es_prestador: userType.value === 'prestador',
      plan: userType.value === 'prestador' ? selectedPlan.value : 'free',
      perfil: perfilPayload
    };
    
    console.log('Enviando datos de onboarding:', data);
    
    await onboardingService.completeOnboarding(data);
    
    // Avanzar al paso final
    const finalStep = userType.value === 'cliente' ? 3 : 6;
    currentStep.value = finalStep;
  } catch (error) {
    console.error('Error al guardar perfil:', error);
    alert('Error al completar el onboarding. Por favor, intenta de nuevo.');
  }
}

// Procesar pago con MercadoPago
async function procesarPago() {
  procesandoPago.value = true;
  
  try {
    // Primero completar onboarding
    await finishOnboarding();
    
    // Verificar si el plan es gratuito (por código o por precio)
    const planData = subscriptionPlans.value.find(p => p.code === selectedPlan.value);
    const isPlanFree = selectedPlan.value === 'free' || (planData && planData.priceText === 'Gratis') || (planData && parseFloat(planData.priceText) === 0);
    
    if (isPlanFree) {
      console.log('Plan gratuito detectado, activando directamente...');
      // Para planes gratuitos, aún necesitamos activar la suscripción
      try {
        const response = await mercadoPagoService.crearPreferencia(selectedPlan.value);
        console.log('Plan gratuito activado:', response.data);
        // El backend debería devolver is_free: true para planes gratuitos
        if (response.data.is_free) {
          // Plan activado exitosamente, redirigir al dashboard
          goToDashboard();
          return;
        }
      } catch (error) {
        console.error('Error activando plan gratuito:', error);
        alert('Error al activar el plan gratuito. Por favor, intenta de nuevo.');
      }
      return;
    }
    
    // Crear preferencia de MercadoPago
    console.log('Creando preferencia de pago para plan:', selectedPlan.value);
    const response = await mercadoPagoService.crearPreferencia(selectedPlan.value);
    
    console.log('Respuesta de MercadoPago:', response.data);
    
    // Redirigir a MercadoPago
    const initPoint = response.data.init_point;
    if (initPoint) {
      window.location.href = initPoint;
    } else {
      throw new Error('No se recibió URL de pago de MercadoPago');
    }
    
  } catch (error) {
    console.error('Error procesando pago:', error);
    
    let errorMessage = 'Error al procesar el pago. ';
    if (error.response?.data?.error) {
      errorMessage += error.response.data.error;
    } else if (error.message) {
      errorMessage += error.message;
    } else {
      errorMessage += 'Por favor, intenta de nuevo.';
    }
    
    alert(errorMessage);
  } finally {
    procesandoPago.value = false;
  }
}

function goToDashboard() {
  if (userType.value === 'prestador') {
    router.push('/prestador/dashboard');
  } else {
    router.push('/');
  }
}

// Helpers
function isFieldEnabled(fieldName) {
  // Busca el plan seleccionado y revisa fieldsEnabled
  const plan = subscriptionPlans.value.find(p => p.code === selectedPlan.value) || null;
  if (!plan) return false;
  if (!Array.isArray(plan.fieldsEnabled)) return false;
  return plan.fieldsEnabled.includes(fieldName);
}

function isSelectedPlanFree() {
  // Determina si el plan seleccionado es gratuito
  if (!selectedPlan.value) return false;
  
  if (selectedPlan.value === 'free') return true;
  
  const planData = subscriptionPlans.value.find(p => p.code === selectedPlan.value);
  if (!planData) return false;
  
  // Verificar si el precio es 0 o "Gratis"
  return planData.priceText === 'Gratis' || parseFloat(planData.priceText) === 0;
}

function fieldLabel(key) {
  const labels = {
    telefono: 'Teléfono',
    direccion: 'Dirección',
    ciudad: 'Ciudad',
    provincia: 'Provincia',
    sitio_web: 'Sitio web',
    descripcion: 'Descripción',
  };
  return labels[key] || key;
}

function getAllowedPerfilPayload() {
  // Para prestadores, filtrar según fieldsEnabled; para clientes, enviar lo que el usuario completó (teléfono/ciudad)
  const payload = {};
  const entries = Object.entries(profileData.value);
  if (userType.value === 'prestador') {
    entries.forEach(([k, v]) => {
      if (isFieldEnabled(k) && v !== undefined && v !== null && v !== '') {
        payload[k] = v;
      }
    });
  } else {
    // cliente: solo guardamos si lo completó
    entries.forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') {
        payload[k] = v;
      }
    });
  }
  return payload;
}

// Limpiar automáticamente los campos no habilitados cuando cambia el plan
function clearDisallowedProfileFields() {
  if (userType.value !== 'prestador') return;
  const keys = Object.keys(profileData.value || {});
  keys.forEach((k) => {
    if (!isFieldEnabled(k)) {
      profileData.value[k] = '';
    }
  });
}

// Watchers
watch(() => selectedPlan.value, () => {
  // Si el usuario cambia de plan, eliminar valores en campos bloqueados
  clearDisallowedProfileFields();
});

watch(() => selectedCategory.value, () => {
  // Si cambia la categoría, resetear el rubro seleccionado
  selectedRubro.value = null;
});

// Formatear precio por mes si falta el sufijo
function formatPriceText(text) {
  if (!text) return '';
  const lower = String(text).toLowerCase();
  if (lower.includes('/ mes') || lower.includes('por mes') || lower.includes('mensual')) {
    return text;
  }
  return `${text} / mes`;
}
</script>

<style scoped>
/* Todos los estilos están en las clases de Tailwind */
</style>
