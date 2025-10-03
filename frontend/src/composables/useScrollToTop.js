/**
 * Composable para manejar scroll programáticamente
 * Útil para casos específicos donde necesitemos control manual del scroll
 */

import { nextTick } from 'vue'

export function useScrollToTop() {
  /**
   * Scroll suave al top de la página
   * @param {number} delay - Delay en ms antes del scroll (default: 0)
   */
  const scrollToTop = async (delay = 0) => {
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay))
    }
    
    await nextTick()
    
    window.scrollTo({
      top: 0,
      left: 0,
      behavior: 'smooth'
    })
  }

  /**
   * Scroll a un elemento específico
   * @param {string} selector - Selector CSS del elemento
   * @param {number} offset - Offset en pixels desde el top (default: 0)
   */
  const scrollToElement = async (selector, offset = 0) => {
    await nextTick()
    
    const element = document.querySelector(selector)
    if (element) {
      const elementTop = element.offsetTop - offset
      window.scrollTo({
        top: elementTop,
        left: 0,
        behavior: 'smooth'
      })
    } else {
      console.warn(`Element with selector "${selector}" not found`)
    }
  }

  /**
   * Scroll inmediato (sin animación) al top
   */
  const jumpToTop = () => {
    window.scrollTo(0, 0)
  }

  /**
   * Obtener la posición actual del scroll
   */
  const getScrollPosition = () => {
    return {
      x: window.pageXOffset || document.documentElement.scrollLeft,
      y: window.pageYOffset || document.documentElement.scrollTop
    }
  }

  /**
   * Guardar posición actual del scroll
   */
  const saveScrollPosition = () => {
    const position = getScrollPosition()
    sessionStorage.setItem('savedScrollPosition', JSON.stringify(position))
    return position
  }

  /**
   * Restaurar posición guardada del scroll
   */
  const restoreScrollPosition = () => {
    const savedPosition = sessionStorage.getItem('savedScrollPosition')
    if (savedPosition) {
      const position = JSON.parse(savedPosition)
      window.scrollTo(position.x, position.y)
      sessionStorage.removeItem('savedScrollPosition')
      return position
    }
    return null
  }

  return {
    scrollToTop,
    scrollToElement,
    jumpToTop,
    getScrollPosition,
    saveScrollPosition,
    restoreScrollPosition
  }
}
